# -*- coding: utf-8 -*-

import django_filters

from v1.models.Board import Boards


class BoardFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    owner = django_filters.CharFilter(name='owner__username', lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('date_created', 'created'),
            ('date_modified', 'modified'),
        ))

    class Meta:
        model = Boards
        fields = ('name', 'owner', 'ordering', 'deleted')
