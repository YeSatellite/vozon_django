# coding=utf-8
from apps.info.models import Country, Region, City

country = Country.objects.create(name="Казахстана")
region = Region.objects.create(name="Западно-Казахстанская область", country=country)
city = City.objects.create(name="Уральск", region=region)
