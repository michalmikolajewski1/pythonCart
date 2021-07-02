from django.urls import path
from django.contrib import admin
from shop.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Leave as empty string for base url
    path('admin/', admin.site.urls),

    path('', shop, name="shop"),
    path('<int:pk>', product_by_id, name="product"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_product/', update_product, name="update_product"),
    path('process_order/', processOrder, name="process_order")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
