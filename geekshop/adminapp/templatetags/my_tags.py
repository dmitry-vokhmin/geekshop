from django import template
from django.conf import settings


register = template.Library()


@register.filter(name="media_folder_products")
def media_folder_products(string):
    if not string:
        string = "default_image_product.png"
    return f"{settings.MEDIA_URL}{string}"
