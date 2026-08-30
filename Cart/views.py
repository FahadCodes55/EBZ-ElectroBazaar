from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . models import Cart, CartItem
from Products.models import Product
from django.contrib import messages

# Create your views here.

@login_required(login_url='/accounts/login/')
def shopping_cart(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    items = CartItem.objects.filter(cart=cart) if cart else []

    sub_total = float(sum(item.subtotal() for item in items))
    tax = round(sub_total * 0.05, 2)
    shipping = 10.0 if sub_total > 0 else 0.0
    discount = 0.0
    grand_total = round((sub_total + tax + shipping) - discount, 2)

    context = {
        'items': items,
        'sub_total': sub_total,
        'shipping': shipping,
        'discount': discount,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request,'Cart/cart.html', context)


@login_required(login_url='/accounts/login/')
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Always increment if it already exists or was just created
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    # to go the cart page navigation
    # return redirect('shopping-cart')
    messages.success(request, f' {product.name} Successfully Added in Cart!.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login/')
def minus_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('shopping-cart')


def remove_cart(request, product_id):
    item = get_object_or_404(CartItem, id = product_id)
    item.delete()
    return redirect('shopping-cart')