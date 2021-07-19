from mainapp.models import Product
from basketapp.models import Basket
from django.views.generic.list import ListView
from django.views.generic import TemplateView


class IndexListView(ListView):
    model = Product
    template_name = "geekshop/index.html"

    def get_queryset(self):
        return Product.objects.all()[:4]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "магазин"
        if self.request.user.is_authenticated:
            context["basket"] = Basket.objects.filter(user=self.request.user)
        return context


class ContactsListView(TemplateView):
    template_name = "geekshop/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "контакты"
        basket = []
        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user)
        context["basket"] = basket
        context["locations"] = [
            {
                "city": "Москва",
                "phone": "+7-888-888-8888",
                "email": "info@geekshop.ru",
                "address": "В пределах МКАД"
            } for _ in range(3)
        ]
        return context
