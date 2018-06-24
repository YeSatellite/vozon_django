# coding=utf-8
from django.db.models import Q
from rest_framework import filters

from apps.client.models import Route, Order, Offer
from apps.core.utils import norm


class RouteFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        :param view:
        :type request:
        :type queryset: Route.objects
        """
        par = request.query_params
        norm(par)
        type_ = par.get('type', None)
        if f(type_):
            type_ = type_.split(',')
            queryset = queryset.filter(transport__type__in=type_)

        if f(par.get('start_point_c', None)):
            queryset = queryset.filter(start_point__region__country_id=par['start_point_c'])
        elif f(par.get('start_point_r', None)):
            queryset = queryset.filter(start_point__region_id=par['start_point_r'])
        elif f(par.get('start_point', None)):
            queryset = queryset.filter(start_point_id=par['start_point'])

        if f(par.get('end_point', None)):
            queryset = queryset.filter(Q(end_point_id=par['end_point']) | Q(end_point__isnull=True))
        if f(par.get('start_date', None)):
            queryset = queryset.filter(shipping_date__gte=par['start_date'])
        if f(par.get('end_date', None)):
            queryset = queryset.filter(shipping_date__lte=par['end_date'])

        return queryset


class OrderFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        :param view:
        :type request:
        :type queryset: Order.objects
        """
        par = request.query_params
        offers_orders = Offer.objects.all() \
            .filter(transport__owner=request.user) \
            .values_list('order', flat=True)

        status = par.get('status', 'posted')
        if status == 'posted':
            start_point = par.get('start_point', None)
            if f(start_point):
                start_point = start_point.split(',')
                print(start_point)
                queryset = queryset.filter(start_point_id__in=start_point)
            queryset = queryset.filter(offer=None)
            queryset = queryset.exclude(pk__in=offers_orders)
        elif status == 'active':
            offers = Offer.objects.filter(transport__owner=request.user)
            queryset = queryset.filter(offer__in=offers)
        else:
            queryset = queryset.filter(pk__in=offers_orders)
            queryset = queryset.filter(offer__isnull=True)

        return queryset


def f(value):
    return value and value != ['0'] and value != ['']
