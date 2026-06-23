import uuid
from django.db import models


class ProductManager(models.Manager):

    def in_stock(self):
        return self.filter(stock__gt=0)

    def items_by_descending_price(self):
        return self.order_by("-price")

    def items_by_ascending_price(self):
        return self.order_by("price")


class Product(models.Model):

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["price"]),
        ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    attributes = models.ManyToManyField("Attribute")
    image = models.ImageField(upload_to="products/", default="products/default.jpg")

    objects = ProductManager()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to="media", verbose_name="Изображение")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказов"
