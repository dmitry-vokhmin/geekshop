from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserProfileEditForm
from .models import ShopUser
from geekshop import settings


def send_verify_email(user):
    verify_link = reverse("auth:verify", args=[user.email, user.activation_key])
    title = f"Activation for - {user.username}"
    message = f"To activate your account follow the link: \n{settings.DOMAIN_NAME}{verify_link}"
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class VerifyTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        user = ShopUser.objects.filter(email=kwargs["email"]).first()
        if user and user.activation_key == kwargs["activation_key"] and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = ""
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.template_name = "authapp/verification.html"
        return super().get(request, *args, **kwargs)


class Login(LoginView):
    form_class = ShopUserLoginForm
    template_name = "authapp/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "login"
        return context


class RegisterView(CreateView):
    model = ShopUser
    template_name = "authapp/register.html"
    form_class = ShopUserRegisterForm

    def form_valid(self, form):
        self.object = form.save()
        if send_verify_email(self.object):
            print("Message sent")
        else:
            print("Message was not sent")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("auth:email", kwargs={"email": self.object.email})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "registration"
        return context


class ActivationEmailView(TemplateView):
    template_name = "authapp/email_sent.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Activation"
        data["email"] = self.kwargs["email"]
        return data


class UpdateUserView(UpdateView):
    model = ShopUser
    template_name = "authapp/edit.html"
    success_url = reverse_lazy("geekshopapp:index")
    form_class = ShopUserEditForm
    second_form_class = ShopUserProfileEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_2"] = self.second_form_class(instance=self.object.shopuserprofile)
        context["title"] = "edit"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form_2 = self.second_form_class(request.POST, instance=self.object.shopuserprofile)
        if form.is_valid() and form_2.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        return self.request.user
