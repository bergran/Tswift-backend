# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Board import Boards


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Boards
        fields = (
            'id',
            'name',
            'deleted',
            'date_created',
            'date_modified',
            'owner',
            'states'
        )

        read_only_fields = (
            'id',
            'deleted',
            'date_created',
            'date_modified',
            'states',
            'owner'
        )

    def create(self, validated_data):
        return Boards.objects.get_or_create(
            name=validated_data.get('name'),
            owner=self.context.get('user')
        )[0]
