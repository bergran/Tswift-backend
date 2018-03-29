# -*- coding: utf-8 -*-

from django_filters import rest_framework as filters

from groups.models.group_profile import Group


class GroupFilter(filters.FilterSet):
    owner = filters.CharFilter(name='profile__owner__username', lookup_expr='icontains')

    class Meta:
        model = Group
        fields = (
            'owner',
            'name'
        )
