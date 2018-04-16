# -*- coding: utf-8 -*-

import django_filters

from v1.models.Board import Boards


class BoardFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    owner = django_filters.CharFilter(name='owner__username', lookup_expr='icontains')

    class Meta:
        model = Boards
        fields = ('name', 'owner')
