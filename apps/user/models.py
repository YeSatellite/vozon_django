# coding=utf-8
from random import randint

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.core.utils import sms_sender
from apps.user.manager import TYPE, UserManager
from apps.core.models import TimeStampedMixin, SoftDeletionMixin
from apps.info.models import City, Country


class User(AbstractBaseUser,
           PermissionsMixin,
           TimeStampedMixin):
    phone = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, models.CASCADE)
    about = models.CharField(max_length=1000, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    is_staff = models.BooleanField(default=False)  # for admin page
    sms_code = models.CharField(max_length=10, null=True)

    type = models.CharField(max_length=10, choices=TYPE)

    experience = models.PositiveIntegerField(null=True)
    courier_type = models.IntegerField(null=True)
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        full_name = '%s %s' % (self.name, self.phone)
        return full_name.strip()

    def get_short_name(self):
        return self.name

    def send_sms_confirmation(self):
        sms_code = str(randint(0, 9999)).zfill(4)
        phone = self.phone

        if getattr(settings, 'SMS_DEBUG', False):
            if len(phone) > 8 and phone[5:9] == "0000":
                self.sms_code = '0000'
                self.save()
                return None

        sms_sender(phone, sms_code)
        self.sms_code = sms_code
        self.save()

    def rating_add(self, ration):
        if self.type != TYPE[1][1]:
            raise ValidationError('only client, please.')
        self.rating_sum += ration
        self.rating_count += 1
        self.save()
