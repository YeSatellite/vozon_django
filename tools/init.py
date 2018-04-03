# coding=utf-8
from apps.info.models import Country, Region, City

country = Country.objects.create(name="Test")
region = Region.objects.create(name="Test", country=country)
city = City.objects.create(name="Test", region=region)
