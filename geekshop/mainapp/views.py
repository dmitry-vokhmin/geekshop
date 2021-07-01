from django.shortcuts import render
from .models import ProductCategory


def products(request):
    title = "продукты/каталог"
    product_categories = ProductCategory.objects.all()
    products_list = [
        {
            "img": "/static/geekshop/img/product-11.jpg",
            "header": "Стул повышенного качества",
            "text": "Не оторваться."
        },
        {
            "img": "/static/geekshop/img/product-21.jpg",
            "header": "Стул повышенного качества",
            "text": "Не оторваться."
        },
        {
            "img": "/static/geekshop/img/product-31.jpg",
            "header": "Стул повышенного качества",
            "text": "Не оторваться."
        }
    ]
    slider_blocks = [
        {"img": "/static/geekshop/img/controll.jpg"},
        {"img": "/static/geekshop/img/controll1.jpg"},
        {"img": "/static/geekshop/img/controll2.jpg"},
    ]
    context = {
        "title": title,
        "product_categories": product_categories,
        "products_list": products_list,
        "slider_blocks": slider_blocks
    }
    return render(request, "mainapp/products.html", context=context)
