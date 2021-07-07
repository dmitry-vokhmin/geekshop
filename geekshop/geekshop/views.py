from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket


def index(request):
    title = "магазин"
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    products = Product.objects.all()[:4]
    context = {
        "title": title,
        "products": products,
        "basket": basket
    }
    return render(request, "geekshop/index.html", context=context)


def contacts(request):
    title = "контакты"
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    locations = [
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
        {"city": "Москва", "phone": "+7-888-888-8888", "email": "info@geekshop.ru", "address": "В пределах МКАД"},
    ]
    context = {
        "title": title,
        "locations": locations,
        "basket": basket
    }
    return render(request, "geekshop/contact.html", context=context)
