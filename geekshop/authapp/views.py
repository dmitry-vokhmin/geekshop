from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from .forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm
from .models import ShopUser


class Login(LoginView):
    form_class = ShopUserLoginForm
    template_name = "authapp/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "вход"
        return context


class RegisterView(CreateView):
    model = ShopUser
    template_name = "authapp/register.html"
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy("auth:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "регистрация"
        return context


class UpdateUserView(UpdateView):
    model = ShopUser
    template_name = "authapp/edit.html"
    success_url = reverse_lazy("index")
    form_class = ShopUserEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "редактирование"
        return context

    def get_object(self, queryset=None):
        return self.request.user
