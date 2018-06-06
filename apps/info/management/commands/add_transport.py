# coding=utf-8
from django.core.management import BaseCommand
from rest_framework.utils import json

from apps.info.models import Country, Region, City, TransportType, TransportMark, TransportModel


class Command(BaseCommand):
    help = 'add new countries'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            action='store_true',
            dest='force',
            help='Auto clear all location tables',
        )

        parser.add_argument(
            '-i',
            action='store_true',
            dest='ignore',
            help='Ignore if already exist',
        )

    def handle(self, *args, **options):

        with open('tools/data/%s' % "transport.json") as f:
            data = json.load(f)

        if options['force']:
            TransportType.objects.all().delete()
            TransportMark.objects.all().delete()

        if TransportType.objects.all().count():
            raise ValueError('TransportType is not empty')

        if TransportMark.objects.all().count():
            raise ValueError('TransportMark is not empty')

        t_type = data['type']
        marks = data['marks']

        t_dict = {}

        for t in t_type:
            tt = TransportType.objects.create(name=t['name'])
            t_dict[t['id']] = tt

        for mark_ in marks:
            mark = TransportMark.objects.create(name=mark_['name'])
            for model_ in mark_['models']:
                TransportModel.objects.create(name=model_['name'], type=t_dict[model_['type']], mark=mark)

