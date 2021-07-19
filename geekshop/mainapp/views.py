import random
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import ProductCategory, Product
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    product = Product.objects.all()
    return random.sample(list(product), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products


class ProductsListView(ListView):
    model = Product
    template_name = "mainapp/products.html"
    paginate_by = 3

    def get_queryset(self):
        if self.kwargs.get("pk") is None or self.kwargs.get("pk") == 0:
            products_list = Product.objects.filter(is_deleted=False).order_by("price")
        else:
            products_list = Product.objects.filter(is_deleted=False, category__pk=self.kwargs["pk"]).order_by("price")
        return products_list

    def get_context_data(self, *, object_list=None, queryset=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "продукты/каталог"
        context["basket"] = get_basket(self.request.user)
        context["hot_product"] = get_hot_product()
        context["product_categories"] = ProductCategory.objects.filter(is_deleted=False)
        category = ProductCategory.objects.filter(pk=self.kwargs.get("pk", 0)).first()
        context["category"] = category or {"name": "все"}
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "mainapp/product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "продукт"
        context["product_categories"] = ProductCategory.objects.all()
        context["basket"] = get_basket(self.request.user)
        return context
