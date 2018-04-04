# coding=utf-8
from rest_framework import permissions

from apps.user.manager import TYPE


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsItOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == TYPE[0][0]


class IsCourier(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == TYPE[1][1]
