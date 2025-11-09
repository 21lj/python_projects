from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.userSignUp, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.userLogOut, name='logout'),
    path('choice/', views.landing, name='page1'),
    path('home/<int:tid>/', views.home, name='home'),
    path('home/shop/<int:sid>', views.shopFun, name='shopFun'),
    path('snack/<int:snackId>', views.getSnacks, name='getSnacks'),
    path('snack/order/<int:sid>', views.buy_now, name='buyNow'),
    path('home/profile/edit', views.editUserProfile, name='editProfile'),

    path('snack/order/payment', views.processPayment, name='process_payment'),
    
    # OG path('snack/order/<int:order_id>/', views.processPayment, name='order_confirmation'),
    path('snack/order/notify/<int:order_id>/', views.notifyOrderConfirmation, name='notify_order_confirmation'),
   
    path('home/profile/', views.profile, name='profile'),
    path('home/orders/', views.myOrders, name='myorders'),

    path('home/cart/', views.viewCart, name='cart'),
    path('home/cart/details/<int:order_id>/', views.viewCartOrders, name='viewCart'),
    path('home/cart/<int:snack_id>/', views.add2Cart, name='add2cart'),
    path('home/cart/checkout', views.cartDetailsPush2Orders, name='checkout'),
]