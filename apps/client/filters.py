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
        par = {k: lambda x: x[0] for k, v in par.items()}
        norm(par)
        type_ = par.get('type', None)
        if type_ == -1:
            queryset = queryset.filter(transport__isnull=True)
        elif type_:
            queryset = queryset.filter(transport__model__type=type_)
        if f(par.get('start_point', None)):
            queryset = queryset.filter(start_point_id=par['start_point'])
        if f(par.get('end_point', None)):
            queryset = queryset.filter(end_point_id=par['end_point'])
        if f(par.get('start_date', None)):
            queryset = queryset.filter(shipping_date__gte=par['start_date'])
        if f(par.get('end_date', None)):
            queryset = queryset.filter(shipping_date__lte=par['end_date'])

        return queryset


def f(value):
    return value and value != '0'
