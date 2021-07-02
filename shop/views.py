from django.shortcuts import render
from shop.models import *
from django.http import JsonResponse
import json
import datetime


# Create your views here.
def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, is_finalised=False)
        items = order.cartproduct_set.all()
        cartProducts = order.cart_products_number
    else:
        items = []
        order = {'sum_total_cart_price': 0, 'cart_products_number': 0}
        cartProducts = order['cart_products_number']

    context = {
        'items': items,
        'order': order
    }

    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }
    return render(request, 'shop/shop.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, is_finalised=False)
        items = order.cartproduct_set.all()
    else:
        items = []
        order = {'sum_total_cart_price': 0, 'cart_products_number': 0}

    context = {
        'items': items,
        'order': order
    }
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, is_finalised=False)
        cartProduct = order.cartproduct_set.all()
        cartItems = order.cart_products_number
    else:
        cartProduct = []
        order = {'sum_total_cart_price': 0, 'cart_products_number': 0}
        cartItems = order['cart_products_number']

    context = {
        'cartProduct': cartProduct,
        'order': order,
        'cartItems': cartItems

    }
    return render(request, 'shop/checkout.html', context)


def update_product(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Cart.objects.get_or_create(customer=customer, is_finalised=False)
    cartProduct, created = CartProduct.objects.get_or_create(cart=order, product=product)

    if action == 'add':
        cartProduct.quantity = (cartProduct.quantity + 1)
        print('Action add')
        print('Quantity', cartProduct.quantity)
    elif action == 'remove':
        cartProduct.quantity = (cartProduct.quantity - 1)
        print('Action remove')
        print('Quantity', cartProduct.quantity)
    cartProduct.save()

    if cartProduct.quantity <= 0:
        cartProduct.delete()
        print('Action delete')

    return JsonResponse('Product was added', safe=False)


def processOrder(request):
    cart_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['data']['total'])

    if total == 0:
        return JsonResponse('Add one item to cart', safe=False)

    elif request.user.is_authenticated:
        customer = request.user.customer
        order, created = Cart.objects.get_or_create(customer=customer, is_finalised=False)
        order.cart_id = cart_id

        if total == order.sum_total_cart_price:
            order.is_finalised = True
        order.save()

    return JsonResponse('Payment completed', safe=False)


def product_by_id(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,

    }
    return render(request, 'shop/product.html', context)
