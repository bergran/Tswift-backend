# -*- coding: utf-8 -*-

import django_filters

from v1.models.Board import Boards


class BoardFilters(django_filters.FilterSet):
    class Meta:
        model = Boards
        fields = ('name', )
