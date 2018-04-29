# coding=utf-8
from django.db import models

from apps.core.manager import SoftDeletionManager


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeletionMixin(models.Model):
    is_active = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    objects = SoftDeletionManager(True)
    deleted = SoftDeletionManager(False)

    class Meta:
        abstract = True
