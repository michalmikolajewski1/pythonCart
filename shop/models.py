from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'id': self.id})


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    cart_id = models.CharField(max_length=200, null=True)
    is_finalised = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.cart_id)

    @property
    def sum_total_cart_price(self):
        cartproducts = self.cartproduct_set.all()
        total = sum([product.get_total_product_price for product in cartproducts])
        return total

    @property
    def cart_products_number(self):
        cartproducts = self.cartproduct_set.all()
        total = sum([product.quantity for product in cartproducts])
        return total


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    def get_total_product_price(self):
        total = self.product.price * self.quantity
        return total
