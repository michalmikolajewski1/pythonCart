from django.test import TestCase
from django.urls import reverse, resolve
from shop.views import *
from shop.models import *
from Project.urls import *
import pytest
from mixer.backend.django import mixer
from django_fake_model import models as f


# Create your tests here.

class TestUrls:
    def setUp(self):
        Product.objects.create(name='Product1', price='10.0', image='')

    def test_product_url(self):
        path = reverse('product', kwargs={'pk': 1})
        assert resolve(path).view_name == "product"
