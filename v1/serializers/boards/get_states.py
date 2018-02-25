# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Board import Boards
from v1.serializers.tasks_states.serializer import StateSerializer


class GetStatesSerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ('id', 'name', 'states')
