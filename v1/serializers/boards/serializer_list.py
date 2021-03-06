# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Board import Boards


class BoardListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Boards
        fields = (
            'id',
            'name',
            'deleted',
            'date_created',
            'date_modified',
            'owner'
        )


