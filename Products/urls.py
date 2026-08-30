from django.urls import path
from .import views
urlpatterns = [
    path('laptops/', views.list_laptop, name='list_laptop'),
    path('laptops/<int:product_id>/', views.laptop, name='laptop'),

    path('phones/', views.list_phone, name='list_phone'),
    path('phones/<int:product_id>/', views.phone, name='phone'),


    path('accessories/', views.list_accessories, name='accessories'),
    path('accessories/<int:product_id>/', views.accessory, name='accessory'),

    path('home-electronics/', views.list_electronics, name='electronics'),
    path('electronic/<int:product_id>/', views.electronic, name='electronic'),

    path('product-detail/<int:product_id>/', views.product_detail, name='product-detail'),
]
