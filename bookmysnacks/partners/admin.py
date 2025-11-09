from django.contrib import admin
from .models import Shop, Snacks, Category, Orders, OrderDetail, Payment

# Register your models here.
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Snacks)
admin.site.register(OrderDetail)
admin.site.register(Orders)
admin.site.register(Payment)