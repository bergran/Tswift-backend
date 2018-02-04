# -*- coding: utf-8 -*-

from rest_framework import serializers


class ChangeNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)