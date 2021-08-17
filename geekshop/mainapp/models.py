from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="name", max_length=64, unique=True)
    description = models.TextField(verbose_name="description", max_length=200, blank=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"category with id - {self.pk}"

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="категория")
    name = models.CharField(verbose_name="Product name", max_length=128)
    image = models.ImageField(upload_to="product_images", blank=True, verbose_name="изображение")
    short_desc = models.CharField(verbose_name="Short description", max_length=100, blank=True)
    description = models.TextField(verbose_name="description", max_length=200, blank=True)
    price = models.DecimalField(verbose_name="Price", max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name="Item amount in a warehouse", default=0)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"product with id - {self.pk}"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_deleted=False).order_by('category', 'name')

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
