import random
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from .models import ProductCategory, Product


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
        context["product"] = get_hot_product()
        context["product_categories"] = ProductCategory.objects.filter(is_deleted=False)
        category = ProductCategory.objects.filter(pk=self.kwargs.get("pk", 0)).first()
        context["category"] = category or {"name": "все"}
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "mainapp/products.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "продукт"
        context["product_categories"] = ProductCategory.objects.filter(is_deleted=False)
        return context


class ProductDetailViewAjax(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = {
                "product_categories": ProductCategory.objects.filter(is_deleted=False),
                "product": Product.objects.filter(pk=self.kwargs["pk"]).first()
            }
            result = render_to_string(
                "mainapp/includes/inc_products_list_content.html",
                context=context,
                request=request
            )
            return JsonResponse({'result': result})
