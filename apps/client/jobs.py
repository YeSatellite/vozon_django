# coding=utf-8
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule

from apps.client.models import Order
from apps.core.utils import norm


class ClearOrderJob(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'client.ClearOrderJob'

    def do(self):
        how_many_days = 1
        orders = Order.objects.filter(shipping_date__lte=datetime.now() - timedelta(days=how_many_days))
        norm("deleted: %d" % len(orders))
        orders.delete()
