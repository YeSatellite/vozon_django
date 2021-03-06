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

        queryset_c = None
        queryset_r = None
        queryset__ = None
        start_point = par.get('start_point_c', None)
        if f(start_point):
            start_point = start_point.split(',')
            queryset_c = queryset.filter(start_point__region__country_id__in=start_point)
        start_point = par.get('start_point_r', None)
        if f(start_point):
            start_point = start_point.split(',')
            queryset_r = queryset.filter(start_point__region_id__in=start_point)
        start_point = par.get('start_point', None)
        if f(start_point):
            start_point = start_point.split(',')
            queryset__ = queryset.filter(start_point_id__in=start_point)

        if not (queryset_c is None and queryset_r is None and queryset__ is None):
            queryset = queryset.none()
            if queryset_c:
                queryset = queryset.union(queryset_c)
            if queryset_r:
                queryset = queryset.union(queryset_r)
            if queryset__:
                queryset = queryset.union(queryset__)
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

            queryset_c = None
            queryset_r = None
            queryset__ = None
            start_point = par.get('start_point_c', None)
            if f(start_point):
                start_point = start_point.split(',')
                queryset_c = queryset.filter(start_point__region__country_id__in=start_point)
            start_point = par.get('start_point_r', None)
            if f(start_point):
                start_point = start_point.split(',')
                queryset_r = queryset.filter(start_point__region_id__in=start_point)
            start_point = par.get('start_point', None)
            if f(start_point):
                start_point = start_point.split(',')
                queryset__ = queryset.filter(start_point_id__in=start_point)

            if not(queryset_c is None and queryset_r is None and queryset__ is None):
                queryset = queryset.none()
                if queryset_c:
                    queryset = queryset.union(queryset_c)
                if queryset_r:
                    queryset = queryset.union(queryset_r)
                if queryset__:
                    queryset = queryset.union(queryset__)
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
