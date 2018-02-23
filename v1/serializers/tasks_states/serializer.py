# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.State import States


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = (
            'id',
            'name',
            'deleted',
            'date_created',
            'date_modified'
        )
        read_only_fields = (
            'id',
            'deleted',
            'date_created',
            'date_modified'
        )