# -*- coding: utf-8 -*-

from django_filters import rest_framework as filters

from v1.models.GroupBoardPermissions import GroupBoardPermissions


class GroupFilters(filters.FilterSet):
    permission = filters.CharFilter(
        label='permission',
        name='permission__name',
        lookup_expr='icontains'
    )
    group = filters.CharFilter(
        label='group',
        name='group__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = GroupBoardPermissions
        fields = ('permission', 'group', )
