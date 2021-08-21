from django.contrib import admin
from .models import Products ,OrderItem , Order , CheckoutAddress , Payment
# Register your models here.

admin.site.register(Products)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)

