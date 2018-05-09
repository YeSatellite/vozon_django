# coding=utf-8
from django_cron import CronJobBase, Schedule

from apps.core.utils import norm


class ClearOrderJob(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'client.ClearOrderJob'

    def do(self):
        norm("Hello From Saṃsāra")

