from django.urls import path
from .views import ProductDetailView, ProductsListView, ProductDetailViewAjax
from django.views.decorators.cache import cache_page

app_name = "mainapp"

urlpatterns = [
    path("", ProductsListView.as_view(), name="index"),
    path("category/<int:pk>/", ProductsListView.as_view(), name="category"),
    path("category/<int:pk>/page/<int:page>/", ProductsListView.as_view(), name="page"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("product/<int:pk>/ajax/", cache_page(3600)(ProductDetailViewAjax.as_view()))
]
