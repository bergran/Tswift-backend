# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.db import IntegrityError
from rest_framework import serializers

from groups.models.group_profile import GroupProfile


class GroupProfileSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')

    def create(self, validated_data):
        owner = self.context.get('user')
        try:
            return GroupProfile.objects.create(
                name=validated_data.get('name'),
                owner=owner
            )
        except IntegrityError:
            raise serializers.ValidationError('Duplicated name error')

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        owner = validated_data.get('owner', instance.owner)
        if instance.name == name:
            instance.name = name
            instance.save()

        if instance.owner == owner:
            instance.owner = owner
            instance.profile.save()
        return instance

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'owner'
        )
        read_only_fields = (
            'id',
            'owner'
        )