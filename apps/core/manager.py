from django.db import models


class SoftDeletionManager(models.Manager):
    active_type = None

    def __init__(self, active_type=True):
        super().__init__()
        self.active_type = active_type

    def get_queryset(self):
        return super().get_queryset().filter(is_active=self.active_type)
