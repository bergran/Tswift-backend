# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.Permissions import READ, WRITE, DELETE, Permissions


class BoardAddUserSerializer(serializers.ModelSerializer):
    users = serializers.ListField(
        child=serializers.CharField(),
        help_text='Users nickname that you want to invite to the board'
    )
    permissions = serializers.MultipleChoiceField(
        choices=[
            READ,
            WRITE,
            DELETE
        ]
    )

    def get_permissions(self, selected):
        return Permissions.objects.filter(
            name__in=selected
        )

    def validate_users(self, users):
        if len(users) > 10:
            raise serializers.ValidationError(
                'Max users per try, max 10'
            )

        users_instance = User.objects.filter(
            username__in=users
        )

        if self.context.get('user') in users_instance:
            raise serializers.ValidationError(
                'Cannot add self to board'
            )

        if users_instance.count() != len(users):
            raise serializers.ValidationError(
                'Users duplicated'
            )
        return users_instance

    def validate_permissions(self, permissions):
        if len(permissions) > 0:
            return self.get_permissions(permissions)
        raise serializers.ValidationError('You should add any permission')

    def validate(self, attrs):
        if self.context.get('user') != self.context.get('board').owner:
            raise serializers.ValidationError('Only onwer can add users')
        return attrs

    def create(self, validated_data):
        board_instance = self.context.get('board')
        users = validated_data.get('users')
        permissions = validated_data.get('permissions')
        UserBoardPermissions.objects.filter(
            user__in=users,
            board=board_instance,
            permission__in=permissions
        ).delete()

        UserBoardPermissions.objects.bulk_create(
            [
                UserBoardPermissions(
                    user=user,
                    board=board_instance,
                    permission=permission
                )
                for user in validated_data.get('users')
                for permission in validated_data.get('permissions')
            ]
        )
        return self.get_initial()

    class Meta:
        model = UserBoardPermissions
        fields = ('id', 'users', 'permissions')
        read_only_fields = (
            'id',
        )
