# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission


class BoardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        groups = request.user.groups.all()
        is_in_groups = obj.groupboardpermissions_set.filter(group__in=groups).exists()
        is_in_users = obj.userboardpermissions_set.filter(user=user).exists()
        return obj.owner == user or is_in_groups or is_in_users

