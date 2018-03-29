# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.db import IntegrityError
from rest_framework import serializers

from groups.models.group_profile import GroupProfile


class GroupProfileSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    def create(self, validated_data):
        owner = self.context.get('user')
        try:
            group = GroupProfile.objects.create_group(
                name=validated_data.get('name'),
                owner=owner
            )
            group.users.add(owner)
            return group
        except IntegrityError:
            raise serializers.ValidationError('Duplicated name error')

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if instance.name != name:
            try:
                instance.name = name
                instance.save()
            except IntegrityError:
                raise serializers.ValidationError('Name exists')
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
