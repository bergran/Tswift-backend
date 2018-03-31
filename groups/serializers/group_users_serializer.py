# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers

from groups.models.group_profile import Group


class GroupUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    def validate_users(self, users):
        group = self.context.get('group')
        if group.users.filter(
            pk__in=[user.pk for user in users]
        ).exists() and self.context.get('action') == 'add_users':
            raise serializers.ValidationError('Users duplicated')
        return users

    def create(self, validated_data):
        group = self.context.get('group')
        users = validated_data.get('users')
        group.users.add(*users)
        return validated_data

    def remove_users(self):
        group = self.context.get('group')
        users = self.validated_data.get('users')

        group.users.remove(*users)
        return users

    class Meta:
        model = Group
        fields = ('users', )

