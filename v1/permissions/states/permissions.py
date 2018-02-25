# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_framework.permissions import BasePermission


class StatesPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in [
            'get_tasks',
            'retrieve',
        ]:
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
        if obj.board.owner == user:
            return True
        elif obj.board.groupboardpermissions_set.filter(
            group__in=user.groups.all(),
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return True
        elif obj.board.userboardpermissions_set.filter(
            user=user,
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return True
        return False
