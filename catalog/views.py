from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from .models import Product, Contact
from .forms import ProductForm

class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    paginate_by = 5
    ordering = ["-created_at"]

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

class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:home")