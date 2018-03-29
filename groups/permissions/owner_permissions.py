# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in [
            'update',
            'partial_update',
            'destroy',
            'add_users',
            'delete_users'
        ]:
            return obj.owner == request.user

        return True
