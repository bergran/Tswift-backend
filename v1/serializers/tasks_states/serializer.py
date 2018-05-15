# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.State import States
from v1.models.Board import Boards
from v1.models.Permissions import READ, WRITE


class StateSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(
        queryset=Boards.objects.all()
    )

    def validate_board(self, board):
        user = self.context.get('user')
        permissions_name = [READ, WRITE]
        if not Boards.permissions.has_boards_access(
                user,
                board,
                permissions_name
        ):
            raise serializers.ValidationError('Invalid board')
        return board

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
