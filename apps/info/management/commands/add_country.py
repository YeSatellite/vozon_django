# coding=utf-8
from django.core.management import BaseCommand
from rest_framework.utils import json

from apps.info.models import Country, Region, City


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
        countries = ['kazakstan.json', 'russian.json', 'kyrgyzstan.json', 'armeniya.json',
                     'uzbekistan.json', 'armeniya.json', ]

        for file in countries:
            with open('tools/data/%s' % file) as f:
                country_ = json.load(f)

            if options['force']:
                Country.objects.filter(name=country_["name"]).delete()

            if Country.objects.filter(name=country_["name"]).count():
                if options['ignore']:
                    continue
                raise ValueError('Country %s already exist' % country_["name"])

            country = Country.objects.create(name=country_["name"], phone_code="+7", phone_mask="todo")
            for region_ in country_["children"]:
                region = Region.objects.create(name=region_["name"], country=country)
                for city_ in region_["children"]:
                    City.objects.create(name=city_, region=region)
