from django.conf import settings
from django.db import models
from mainapp.models import Product


class OrderItemQuerySet(models.QuerySet):
    def delete(self):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super().delete()


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDERS_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent to proceed'),
        (PAID, 'paid'),
        (PROCEEDED, 'proceeded'),
        (READY, 'ready'),
        (CANCEL, 'cancel'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name='created',
        auto_now_add=True,
    )
    update = models.DateTimeField(
        verbose_name='update',
        auto_now=True,
    )
    status = models.CharField(
        verbose_name='status',
        max_length=3,
        choices=ORDERS_STATUS_CHOICES,
        default=FORMING,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
    )

    def __str__(self):
        return f'Current order: {self.id}'

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    # objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        verbose_name='product',
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='quantity',
        default=0,
    )

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    def get_product_cost(self):
        return self.product.price * self.quantity

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(using=None, keep_parents=False)
