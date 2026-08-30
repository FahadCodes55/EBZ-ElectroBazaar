from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Category, Product
# Create your views here.

def list_laptop(request):
    category_laptops = get_object_or_404(Category, name='Laptops')
    products = Product.objects.filter(category=category_laptops)
    return render(request, 'Products/Laptops/laptops_home.html', {'products': products})

def laptop(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    return render(request, 'Products/Laptops/product-detail.html', {'product': product})

def list_phone(request):
    category_phones = get_object_or_404(Category, name = 'Phones')
    products = Product.objects.filter(category = category_phones)
    return render(request, 'Products/Phones/phones_home.html', {'products': products})

def phone(request, product_id):
    item = get_object_or_404(Product, id = product_id)
    return render(request, 'Products/Laptops/product-detail.html', {'product': item})


def list_accessories(request):
    category_accessories = get_object_or_404(Category, name = 'Accessories')
    products = Product.objects.filter(category = category_accessories)
    return render(request, 'Products/Accessories/accessories_home.html', {'product' : products})

def accessory(request, product_id):
    item = get_object_or_404(Product, id = product_id)
    return render(request, 'Products/Laptops/product-detail.html', {'product': item})

def list_electronics(request):
    category_electronics = get_object_or_404(Category, name = 'electronics')
    products = Product.objects.filter(category = category_electronics)
    return render(request, 'Products/HomeElectronics/home_electronics.html', {'product' : products})

def electronic(request, product_id):
    item = get_object_or_404(Product, id = product_id)
    return render(request, 'Products/Laptops/product-detail.html', {'product': item})

def product_detail(request, product_id):
    single_item = get_object_or_404(Product, id=product_id)
    return render(request, 'Products/Laptops/product-detail.html', {'item': single_item})