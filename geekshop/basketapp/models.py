from django.db import models
from geekshop import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class BasketQuerySet(models.QuerySet):

    def delete(self):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="quantity", default=0)
    is_deleted = models.BooleanField(default=False)
    add_datetime = models.DateTimeField(verbose_name="date", auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = self.get_items_cached
        _total_cost = _items.annotate(cost=models.F("product__price") * models.F("quantity")).aggregate(models.Sum(models.F("cost")))
        # _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost["cost__sum"]

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(using=None, keep_parents=False)
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)
