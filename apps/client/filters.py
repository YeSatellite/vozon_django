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
        if type_ is not None:
            queryset = queryset.filter(transport__type=par['type'])
        else:
            queryset = queryset.filter(transport__isnull=True)
        queryset = queryset.filter(start_point_id=par['start_point'])
        queryset = queryset.filter(end_point_id=par['end_point'])
        queryset = queryset.filter(shipping_date__range=[par['start_date'], par['end_date']])
        return queryset
