from django.urls import path
from .views import IndexListView, ContactsListView

app_name = "geekshopapp"

urlpatterns = [
    path('', IndexListView.as_view(), name="index"),
    path('contacts/', ContactsListView.as_view(), name="contacts"),
]
