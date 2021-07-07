from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import Sum
from .models import Basket
from mainapp.models import Product


def basket(request):
    if request.user.is_authenticated:
        total_sum = 0
        basket_db = Basket.objects.filter(user=request.user)
        quantity_sum = basket_db.aggregate(Sum("quantity"))
        for itm in basket_db:
            total_sum += itm.count_sum()
        context = {
            "basket": basket_db,
            "quantity_sum": quantity_sum["quantity__sum"],
            "total_sum": total_sum
        }
        return render(request, "basketapp/basket.html", context)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket_db = Basket.objects.filter(user=request.user, product=product).first()
    if not basket_db:
        basket_db = Basket(user=request.user, product=product)
    basket_db.quantity += 1
    basket_db.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def basket_remove(request, pk):
    return render(request, "basketapp/basket.html")
