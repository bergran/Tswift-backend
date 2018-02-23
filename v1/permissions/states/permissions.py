# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_framework.permissions import BasePermission


class BoardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            user = request.user
            is_owner = user.boards_set.filter(pk=obj.pk).exists()
            has_group_perm = obj.groupboardpermissions_set.filter(
                group__in=user.groups.all(), permission__name='read'
            ).exists()
            has_user_perm = obj.userboardpermissions_set.filter(
                user=user, permission__name='read'
            ).exists()
        elif view.action == 'destroy':
            user = request.user
            is_owner = user.boards_set.filter(pk=obj.pk).exists()
            has_group_perm = obj.groupboardpermissions_set.filter(
                Q(group__in=user.groups.all()) &
                Q(permission__name__in=['delete', 'read'])
            ).count() == 2
            has_user_perm = obj.userboardpermissions_set.filter(
                Q(user=user) &
                Q(permission__name__in=['delete', 'read'])
            ).count() == 2
        elif view.action == 'change_name':
            user = request.user
            is_owner = user.boards_set.filter(pk=obj.pk).exists()
            has_group_perm = obj.groupboardpermissions_set.filter(
                Q(group__in=user.groups.all()) &
                Q(permission__name__in=['delete', 'read', 'write'])
            ).count() == 3
            has_user_perm = obj.userboardpermissions_set.filter(
                Q(user=user) &
                Q(permission__name__in=['delete', 'read', 'write'])
            ).count() == 3
        elif view.action == 'get_states':
            user = request.user
            is_owner = user.boards_set.filter(pk=obj.pk).exists()
            has_group_perm = obj.groupboardpermissions_set.filter(
                Q(group__in=user.groups.all()) &
                Q(permission__name__in=['read'])
            ).exists()
            has_user_perm = obj.userboardpermissions_set.filter(
                Q(user=user) &
                Q(permission__name__in=['read'])
            ).exists()
        else:
            return True
        return is_owner or has_group_perm or has_user_perm
