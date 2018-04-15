# -*- coding: utf-8 -*-

import django_filters

from v1.models.Board import Boards


class BoardFilters(django_filters.FilterSet):
    owner = django_filters.CharFilter(name='owner__username')

    class Meta:
        model = Boards
        fields = ('name', 'owner')
