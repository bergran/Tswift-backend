# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Permissions import Permissions


class PermissionListSerializer(serializers.ModelSerializer):
    boards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Permissions
        fields = ('groups', 'boards')
