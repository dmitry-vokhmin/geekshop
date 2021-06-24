from django.shortcuts import render


def index(request):
    title = "магазин"
    block_items = [
        {"img": "/static/geekshop/img/product-1.jpg", "header": "Отличный стул", "text": "Расположитесь комфортно."},
        {"img": "/static/geekshop/img/product-2.jpg", "header": "Стул повышенного качества", "text": "Не оторваться."},
    ]
    context = {
        "title": title,
        "block_items": block_items
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
