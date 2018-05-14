# -*- coding: utf-8 -*-

from django_filters import rest_framework as filters

from v1.models.UserBoardPermissions import UserBoardPermissions


class UserFilters(filters.FilterSet):
    permission = filters.CharFilter(
        label='permission',
        name='permission__name',
        lookup_expr='icontains'
    )
    user = filters.CharFilter(
        label='user',
        name='user__username',
        lookup_expr='icontains'
    )

    class Meta:
        model = UserBoardPermissions
        fields = ('permission', 'user', )
