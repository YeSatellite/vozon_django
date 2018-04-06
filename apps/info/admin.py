# coding=utf-8
from django.contrib import admin

from .models import *

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(TransportType)
admin.site.register(TransportMark)
admin.site.register(TransportModel)
admin.site.register(TransportBody)
admin.site.register(TransportShippingType)
admin.site.register(PaymentType)
admin.site.register(OtherService)
