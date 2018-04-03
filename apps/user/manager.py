# coding=utf-8
from django.contrib.auth.base_user import BaseUserManager

from apps.core.manager import SoftDeletionManager
from apps.info.models import City, Country

TYPE = (
    ('client', 'client'),
    ('carrier', 'carrier'),
)


class UserManager(BaseUserManager, SoftDeletionManager):
    use_in_migrations = True

    def _create_user(self, phone, name, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        if not name:
            raise ValueError('The given name must be set')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, name, password=None, **extra_fields):
        return self._create_user(phone, name, password, **extra_fields)

    def create_superuser(self, phone, name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('city', City.objects.all()[0])
        extra_fields.setdefault('citizenship', Country.objects.all()[0])
        extra_fields.setdefault('citizenship', Country.objects.all()[0])
        extra_fields.setdefault('dob', '1996-3-14')
        extra_fields.setdefault('type', TYPE[0][0])

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, name, password, **extra_fields)
