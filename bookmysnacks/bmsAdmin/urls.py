from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.AdminLog, name="login"),
    path('home/', views.Home, name="home"),
    path('add-category/', views.addCategory, name="addCategory"),
    path('add-location/', views.addLocation, name="addLoc"),
    path('manage-category/', views.viewAndManageCategory, name="viewCategory"),
    path('manage-locations/', views.viewAndManageLocation, name="viewLoc"),
    path('view-users/', views.viewUsers, name="viewUsers"),
    path('view-theater/', views.showTheaters, name="viewTheater"),
    path('manage-category/delete/<int:catId>', views.deleteCategory, name="deleteCategory"),
    path('manage-category/edit/<int:catId>', views.editCategory, name="editCategory"),
    path('logout/', views.adminLogOut, name="logout"),
]