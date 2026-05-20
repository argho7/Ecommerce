from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:slug>', category_view, name='category_url'),
    path('product/<slug:slug>', product_view, name='product_detail'),
    path('search/', search, name='search'),

    path('cart/', cart, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile', profile, name='profile'),
    
    path('buy/<int:product_id>/', buy_now, name='buy_now'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/fail/', payment_fail, name='payment_fail'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
    path('payment/gateway/fail/', payment_gate_auth_fail, name='payment_gate_auth_fail'),
]