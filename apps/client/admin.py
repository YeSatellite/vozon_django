# coding=utf-8
from django.contrib import admin

# Register your models here.
from apps.client.models import Order, Offer, Transport

admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(Transport)
