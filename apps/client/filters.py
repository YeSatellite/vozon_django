# coding=utf-8
from rest_framework import filters

from apps.client.models import Route


class RouteFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        :param view:
        :type request:
        :type queryset: Route.objects
        """
        par = request.query_params
        type_ = par.get('type', None)
        if type_ == -1:
            queryset = queryset.filter(transport__isnull=True)
        elif type_:
            queryset = queryset.filter(transport__model__type=type_)
        if par.get('start_point', None):
            queryset = queryset.filter(start_point_id=par['start_point'])
        if par.get('end_point', None):
            queryset = queryset.filter(end_point_id=par['end_point'])
        if par.get('start_date', None):
            queryset = queryset.filter(shipping_date__gte=[par['start_date']])
        if par.get('end_date', None):
            queryset = queryset.filter(shipping_date__lte=[par['end_date']])

        return queryset
