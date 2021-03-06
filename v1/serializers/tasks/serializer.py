# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Task import Tasks
from v1.models.Board import Boards


class TasksSerializer(serializers.ModelSerializer):

    def validate_board(self, board):
        user = self.context.get('user')
        if Boards.permissions.has_boards_access(
            user,
            board
        ):
            return board
        raise serializers.ValidationError('Invalid board')

    def validate(self, attrs):
        board = attrs.get('board')
        state = attrs.get('state')

        if self.instance and state and self.instance.board == state:
                raise serializers.ValidationError('State is not in board')
        elif self.instance:
            return attrs

        if state and state.board != board:
            raise serializers.ValidationError('State is not in board')
        elif not state:
            return attrs

        return attrs

    class Meta:
        model = Tasks
        fields = (
            'id',
            'title',
            'description',
            'date_created',
            'date_modified',
            'date_expired',
            'deleted',
            'state',
            'board'
        )
        read_only_fields = (
            'id',
            'date_created',
            'date_modified',
            'deleted'
        )
