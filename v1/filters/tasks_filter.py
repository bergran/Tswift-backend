# -*- coding: utf-8 -*-

from django.utils.datetime_safe import datetime

import django_filters
import coreapi

from v1.models.Task import Tasks


class TasksFilter(django_filters.FilterSet):
    start_date = django_filters.IsoDateTimeFilter(
        name='date_created',
        lookup_expr='gte'
    )
    end_date = django_filters.IsoDateTimeFilter(
        name='date_created',
        lookup_expr='lte'
    )
    is_expired = django_filters.BooleanFilter(
        method='get_is_expired'
    )
    title = django_filters.CharFilter(
        name='title',
        lookup_expr='contains'
    )


    def get_is_expired(self, queryset, name, value):
        if value:
            return queryset.filter(
                date_expired__lte=datetime.now()
            )
        else:
            return queryset.filter(
                date_expired__gte=datetime.now()
            )

    class Meta:
        model = Tasks
        fields = (
            'start_date',
            'end_date',
            'is_expired',
            'title',
            'deleted'
        )
