from django.contrib import admin
from . models import Login,User, Theater, Location

# Register your models here.
admin.site.register(User)
admin.site.register(Login)
admin.site.register(Theater)
admin.site.register(Location)
