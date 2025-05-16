from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, TemplateView, DetailView,
    CreateView, UpdateView, DeleteView,
)
from .models import Product, Contact
from .forms import ProductForm


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    mod_group_name = "Модератор продуктов"

    def test_func(self) -> bool:
        obj = self.get_object()
        user = self.request.user
        return (
            user == getattr(obj, "owner", None)
            or user.groups.filter(name=self.mod_group_name).exists()
        )


class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contacts"] = Contact.objects.all()
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.object.pk])


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class ProductUnpublishView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, UpdateView):
    """Модератор или владелец может снять товар с публикации."""
    model = Product
    fields = []                                   # форму не показываем
    template_name = "catalog/product_confirm_unpublish.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_published = False
        obj.save(update_fields=["is_published"])
        return super().form_valid(form)
