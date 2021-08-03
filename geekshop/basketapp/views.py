from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import View, DeleteView
from .models import Basket
from mainapp.models import Product


class BasketListView(LoginRequiredMixin, ListView):
    model = Basket
    template_name = "basketapp/basket.html"
    context_object_name = "basket_items"

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).order_by("product__category")


class BasketCreateView(LoginRequiredMixin, View):
    model = Product

    def get(self, request, *args, **kwargs):
        if "login" in self.request.META.get("HTTP_REFERER"):
            return HttpResponseRedirect(reverse("products:product", args=[self.kwargs["pk"]]))
        product = get_object_or_404(self.model, pk=self.kwargs["pk"])
        basket_db = Basket.objects.filter(user=self.request.user, product=product).first()
        if not basket_db:
            basket_db = Basket(user=self.request.user, product=product)
        basket_db.quantity += 1
        basket_db.save()
        return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))


class BasketDeleteView(LoginRequiredMixin, DeleteView):
    model = Basket
    template_name = "basketapp/basket_delete.html"
    success_url = reverse_lazy("basket:view")


class BasketEditView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            quantity = int(self.kwargs["quantity"])
            new_basket_item = Basket.objects.get(pk=int(self.kwargs["pk"]))
            if quantity > 0:
                new_basket_item.quantity = quantity
                new_basket_item.save(update_fields=["quantity"])
            else:
                new_basket_item.delete()
            basket_items = Basket.objects.filter(user=request.user).order_by("product__category")
            context = {
                "basket_items": basket_items
            }
            result = render_to_string("basketapp/includes/inc_basket_list.html", context)
            return JsonResponse({"result": result})
