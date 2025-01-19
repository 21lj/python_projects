from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_U, name='logout'),
    path('delete/<str:name>/',views.delete, name='delete'),
    path('update/<str:name>/', views.update, name='update')
]