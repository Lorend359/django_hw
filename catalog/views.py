from django.shortcuts import render
from .models import Product, Contact

def home(request):
    latest = Product.objects.order_by("-created_at")[:5]
    print(">>> Latest 5 products:", list(latest))
    return render(request, "catalog/home.html", {
        "latest_products": latest,
    })

def contacts(request):
    contacts = Contact.objects.all()
    return render(request, "catalog/contacts.html", {
        "contacts": contacts,
    })
