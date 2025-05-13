from django.urls import path
from .views import (
    HomeListView,
    ContactsView,
    ProductDetailView,
    AddProductView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add/", AddProductView.as_view(), name="add_product"),
]
