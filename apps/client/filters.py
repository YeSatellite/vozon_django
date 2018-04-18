# coding=utf-8
from rest_framework import filters


class RouteFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        par = request.query_params
        queryset = queryset.filter(transport__type_id=par['type'])
        queryset = queryset.filter(start_point_id=par['start_point'])
        queryset = queryset.filter(end_point_id=par['end_point'])
        queryset = queryset.filter(shipping_date__range=[par['start_date'], par['end_date']])
        return queryset
