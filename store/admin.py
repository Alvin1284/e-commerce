from django.contrib import admin
from . import models


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','category', 'inventory']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name','last_name','email']

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Product,AdminProduct)
admin.site.register(models.Customer,AdminCustomer)
admin.site.register(models.Order)