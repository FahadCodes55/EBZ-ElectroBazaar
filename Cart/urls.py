from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart, name='shopping-cart'),
    path('add/<int:product_id>', views.add_cart, name='add_cart'),
    path('minus/<int:product_id>', views.minus_cart, name='minus_cart'),
    path('remove/<product_id>/', views.remove_cart, name='remove_cart'),
]