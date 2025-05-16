from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, TemplateView, DetailView,
                                   CreateView, UpdateView, DeleteView)

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings

from .models import Product, Contact
from .forms import ProductForm
from catalog.services import products_for_category


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    mod_group_name = "Модератор продуктов"

    def test_func(self):
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

    # ⬇️ низкоуровневый кэш
    def get_queryset(self):
        page = self.request.GET.get("page", 1)
        cache_key = f"home_page_qs_{page}"

        qs = cache.get(cache_key)
        if qs is None:
            qs = (super()
                  .get_queryset()
                  .filter(is_published=True)
                  .select_related("category", "owner"))
            cache.set(cache_key, qs, settings.CACHE_TTL)
        return qs


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contacts"] = Contact.objects.all()
        return ctx


@method_decorator(cache_page(settings.CACHE_TTL), name="dispatch")
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


class ProductUpdateView(LoginRequiredMixin,
                         OwnerOrModeratorRequiredMixin,
                         UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.object.pk])


class ProductDeleteView(LoginRequiredMixin,
                         OwnerOrModeratorRequiredMixin,
                         DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")


class ProductUnpublishView(LoginRequiredMixin,
                            OwnerOrModeratorRequiredMixin,
                            UpdateView):
    model = Product
    fields = []
    template_name = "catalog/product_confirm_unpublish.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_published = False
        obj.save(update_fields=["is_published"])
        return super().form_valid(form)


class CategoryProductsView(TemplateView):
    template_name = "catalog/category_products.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cat_id = self.kwargs["pk"]
        ctx["products"] = products_for_category(cat_id,
                                                ttl=settings.CACHE_TTL)
        return ctx
