from django.contrib import admin
from shop.models import *

# Register your models here.


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)

