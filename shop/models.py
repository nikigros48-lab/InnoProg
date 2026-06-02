import uuid
from django.db import models


class ProductManager(models.Manager):


    def in_stock(self):
        return self.filter(stock__gt=0)
    

    def items_by_descending_price(self):
        return self.order_by('-price')
    

    def items_by_ascending_price(self):
        return self.order_by('price')


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    attributes = models.ManyToManyField('Attribute')

    objects = ProductManager()


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Attribute(models.Model):
    name = models.CharField(max_length=255)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
