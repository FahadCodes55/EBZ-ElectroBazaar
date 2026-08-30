from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),

#     Login urls
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

#     login success url
    path('success/', views.success, name='success'),

#      Contact Form url
    path('contact/', views.contact_form, name='contact_form'),

    # For Google Identity Services => For Google login
    path('auth/google/jwt/', views.google_jwt_login, name='google_jwt_login'),

]

