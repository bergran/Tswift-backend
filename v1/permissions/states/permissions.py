# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_framework.permissions import BasePermission


class StatesPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['get_states', 'retrieve']:
            permissions_name = ['read']
        elif view.action == 'destroy':
            permissions_name = ['delete', 'read']
        elif view.action == 'change_name':
            permissions_name = ['read', 'write']
        else:
            return True
        user = request.user
        if obj.board.owner == user:
            return True
        if obj.board.groupboardpermissions_set.filter(
            group__in=user.groups.all(),
            permission__name__in=permissions_name
        ).count() == len(permissions_name) and view.action != 'update':
            return True
        if obj.board.userboardpermissions_set.filter(
            user=user,
            permission__name__in=permissions_name
        ).count() == len(permissions_name) and view.action != 'update':
            return True
        return False
