from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied  # пригодится, если нужно явно «ронять» 403
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Contact, Product


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    """
    Разрешает действие, если
      • пользователь — владелец объекта, или
      • пользователь входит в группу «Модератор продуктов».
    """

    mod_group_name = "Модератор продуктов"

    def test_func(self) -> bool:
        obj = self.get_object()
        user = self.request.user
        return user == getattr(obj, "owner", None) or user.groups.filter(name=self.mod_group_name).exists()


class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)



class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contacts"] = Contact.objects.all()
        return ctx


class ProductDetailView(DetailView):
    """Просмотр карточки товара — только для авторизованных пользователей"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # фиксируем владельца
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
