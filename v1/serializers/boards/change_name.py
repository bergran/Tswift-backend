# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Board import Boards


class ChangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ('id', 'name', 'date_created', 'deleted')
        read_only_fields = (
            'id',
            'date_created',
            'deleted'
        )
