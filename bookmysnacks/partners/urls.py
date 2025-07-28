from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hello, name='welcome'),
    path('theater', views.theaterLog, name='login'),
    path('shop', views.shopLog, name='shopLogin'),
    path('theater/register', views.registerAsTheater, name='register'),
    path('theater/home', views.theaterHome, name='home'),
    path('theater/logout', views.theaterLogOut, name='logout'),
    path('theater/shop/register', views.regsterShops, name='createmyshop'),
    path('theater/profile', views.theaterProfile, name='profile'),
    path('theater/contact', views.contactShop, name='contact'),
    path('theater/revenue', views.listRevenue, name='trevenue'),
    path('theater/profile/edit', views.editTheaterProfile, name='editProfile'),
    path('theater/shop/delete/<int:spId>', views.deleteShop, name='deleteShop'),
    path('shop/home', views.idkk, name="shopHome"),
    path('theater/manage', views.manageShops, name='manageShops'),
    path('shop/logout', views.shopAdminLogOut, name='shopLogout'),
    path('shop/add', views.addSnacks, name='addSnacks'),
    path('shop/profile', views.shopProfile, name='shopProfile'), 
    path('shop/profile/edit', views.editShopProfile, name='editShopProfile'), 
    path('shop/manage', views.manageSnacks, name='manageSnacks'),
    path('shop/manage/edit/<int:sId>', views.editSnacks, name='editSnacks'),
    path('shop/manage/delete/<int:sId>', views.deleteSnacks, name='deleteSnacks'),
    path('shop/orders', views.viewOrders, name='view-orders'),
    path('shop/revenue', views.trackRevenue, name='revenue'),
    path('shop/manage-orders', views.manageOrders, name='manage-orders'),
    path('shop/manage-orders/accept/<int:order_id>', views.accept_order, name='accept-order'),
    path('shop/manage-orders/reject/<int:order_id>', views.reject_order, name='reject-order'),
]