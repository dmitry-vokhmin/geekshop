from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket


def products(request, pk=None):
    title = "продукты/каталог"
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    product_categories = ProductCategory.objects.all()
    slider_blocks = [
        {"img": "/static/geekshop/img/controll.jpg"},
        {"img": "/static/geekshop/img/controll1.jpg"},
        {"img": "/static/geekshop/img/controll2.jpg"},
    ]
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by("price")
            category = {"name": "все"}
        else:
            products_list = Product.objects.filter(category__pk=pk).order_by("price")
            category = get_object_or_404(ProductCategory, pk=pk)
        context = {
            "title": title,
            "product_categories": product_categories,
            "products_list": products_list,
            "category": category,
            "basket": basket,
            "slider_blocks": slider_blocks
        }
        return render(request, "mainapp/products.html", context=context)
    products_list = Product.objects.all()[:3]
    context = {
        "title": title,
        "product_categories": product_categories,
        "products_list": products_list,
        "basket": basket,
        "slider_blocks": slider_blocks
    }
    return render(request, "mainapp/products.html", context=context)