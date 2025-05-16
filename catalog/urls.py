from django.urls import path

from .views import (
    HomeListView, ContactsView, ProductDetailView,
    AddProductView, ProductUpdateView, ProductDeleteView,
    ProductUnpublishView,         # ← новый
)

app_name = "catalog"

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("add/", AddProductView.as_view(), name="add_product"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"),
    path("<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish",),
]
