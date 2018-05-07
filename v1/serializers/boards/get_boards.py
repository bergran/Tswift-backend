# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models import UserBoardPermissions


class BoardPermissions(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    permission = serializers.CharField(source='permission.name')

    class Meta:
        model = UserBoardPermissions
        fields = ('user', 'permission')
