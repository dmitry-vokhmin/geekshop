import random
from django.shortcuts import render, get_object_or_404
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
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    title = "продукты/каталог"
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
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
            'hot_product': hot_product,
            "same_products": same_products,
            "basket": basket,
            "slider_blocks": slider_blocks
        }
        return render(request, "mainapp/products.html", context=context)
    context = {
        "title": title,
        "product_categories": product_categories,
        'hot_product': hot_product,
        "same_products": same_products,
        "basket": basket,
        "slider_blocks": slider_blocks
    }
    return render(request, "mainapp/products.html", context=context)


def product(request, pk):
    title = "продукты"
    context = {
        "title": title,
        "product_categories": ProductCategory.objects.all(),
        "product": get_object_or_404(Product, pk=pk),
        "basket": get_basket(request.user)
    }
    return render(request, "mainapp/product.html", context)