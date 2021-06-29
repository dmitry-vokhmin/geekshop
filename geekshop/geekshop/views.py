from django.shortcuts import render
from mainapp.models import Product


def index(request):
    title = "магазин"
    products = Product.objects.all()
    context = {
        "title": title,
        "products": products
    }
    return render(request, "geekshop/index.html", context=context)


def contacts(request):
    title = "контакты"
    locations = [
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
    ]
    context = {
        "title": title,
        "locations": locations
    }
    return render(request, "geekshop/contact.html", context=context)
