# coding=utf-8
from rest_framework import filters

from apps.client.models import Route
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
        if type_ == ['-1']:
            norm("$1")
            queryset = queryset.filter(transport__isnull=True)
        elif f(type_):
            norm("$2")
            queryset = queryset.filter(transport__model__type=type_)
        if f(par.get('start_point', None)):
            norm("$3")
            queryset = queryset.filter(start_point_id=par['start_point'])
        if f(par.get('end_point', None)):
            norm("$4")
            queryset = queryset.filter(end_point_id=par['end_point'])
        if f(par.get('start_date', None)):
            norm("$5")
            queryset = queryset.filter(shipping_date__gte=par['start_date'])
        if f(par.get('end_date', None)):
            norm("$6")
            queryset = queryset.filter(shipping_date__lte=par['end_date'])

        return queryset


def f(value):
    return value and value != ['0'] and value != ['']
