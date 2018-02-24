# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.State import States
from v1.models.Board import Boards


class StateSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        queryset=Boards.objects.all()
    )

    def validate_board(self, board):
        user = self.context.get('user')
        permissions_name = ['read', 'write']
        if board.owner == user:
            return board
        elif board.groupboardpermissions_set.filter(
            group__in=user.groups.all(),
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return board
        elif board.userboardpermissions_set.filter(
            user=user,
            permission__name__in=permissions_name
        ).count() == len(permissions_name):
            return board
        raise serializers.ValidationError('Invalid board')

    class Meta:
        model = States
        fields = (
            'id',
            'name',
            'deleted',
            'date_created',
            'date_modified',
            'board'
        )
        read_only_fields = (
            'id',
            'deleted',
            'date_created',
            'date_modified'
        )
