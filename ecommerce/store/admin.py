from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)



