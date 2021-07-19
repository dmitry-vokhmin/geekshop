from django.urls import path
from .views import ProductDetailView, ProductsListView

app_name = "mainapp"

urlpatterns = [
    path("", ProductsListView.as_view(), name="index"),
    path("category/<int:pk>/", ProductsListView.as_view(), name="category"),
    path("category/<int:pk>/page/<int:page>/", ProductsListView.as_view(), name="page"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product")
]
