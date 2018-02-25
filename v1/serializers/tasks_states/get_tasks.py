# -*- coding: utf-8 -*-

from rest_framework import serializers

from v1.models.Task import Tasks


class GetTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = (
            'id',
            'title',
            'date_created',
            'date_modified',
            'date_expired',
            'deleted',
        )