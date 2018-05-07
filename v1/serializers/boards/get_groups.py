# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models import GroupBoardPermissions


class BoardPermissionsGroups(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    permission = serializers.CharField(source='permission.name')

    class Meta:
        model = GroupBoardPermissions
        fields = ('group', 'permission')
