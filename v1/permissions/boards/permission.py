# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_framework.permissions import BasePermission


class BoardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['get_states', 'retrieve']:
            permissions_name = ['read']
        elif view.action == 'destroy':
            permissions_name = ['delete', 'read']
        elif view.action in [
            'change_name',
            'create'
        ]:
            permissions_name = ['read', 'write']
        else:
            permissions_name = ['read', 'write', 'delete']

        user = request.user
        if obj.owner == user:
            return True
        if obj.groupboardpermissions_set.filter(
            group__in=user.groups.all(),
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return True
        if obj.userboardpermissions_set.filter(
            user=user,
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return True
        return False
