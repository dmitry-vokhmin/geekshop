from django.urls import path
from django.contrib.auth.views import LogoutView
from authapp import views as authapp

app_name = "authapp"

urlpatterns = [
    path("login/", authapp.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", authapp.RegisterView.as_view(), name="register"),
    path("edit/", authapp.UpdateUserView.as_view(), name="edit"),
    path("verify/<str:email>/<str:activation_key>/", authapp.VerifyTemplateView.as_view(), name="verify")
]