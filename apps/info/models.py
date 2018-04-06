from django.db import models

from apps.core.models import TimeStampedMixin, SoftDeletionMixin


class Country(TimeStampedMixin,
              SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Region(TimeStampedMixin,
             SoftDeletionMixin):
    country = models.ForeignKey(Country, models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class City(TimeStampedMixin,
           SoftDeletionMixin):
    region = models.ForeignKey(Region, models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s, %s" % (self.name, self.region.name))


class TransportType(TimeStampedMixin,
                    SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)


class TransportMark(TimeStampedMixin,
                    SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)


class TransportModel(TimeStampedMixin,
                     SoftDeletionMixin):
    mark = models.ForeignKey(TransportMark, models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class TransportBody(TimeStampedMixin,
                    SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)


class TransportShippingType(TimeStampedMixin,
                            SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)


class PaymentType(TimeStampedMixin,
                  SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)


class OtherService(TimeStampedMixin,
                   SoftDeletionMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str("%s" % self.name)
