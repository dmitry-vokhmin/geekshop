from django.urls import path
from basketapp import views as basketapp

app_name = "basketapp"

urlpatterns = [
    path("", basketapp.BasketListView.as_view(), name="view"),
    path("add/<int:pk>/", basketapp.BasketCreateView.as_view(), name="add"),
    path("remove/<int:pk>/", basketapp.BasketDeleteView.as_view(), name="remove"),
    path("edit/<int:pk>/<int:quantity>/", basketapp.BasketEditView.as_view(), name="edit")
]
