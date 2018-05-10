# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.Permissions import READ, WRITE, DELETE, Permissions


class BoardAddUserSerializer(serializers.ModelSerializer):
    users = serializers.ListField(
        child=serializers.JSONField(),
        help_text='Users nickname that you want to invite to the board'
    )

    def check_name(self, user):
        if 'name' not in user:
            raise serializers.ValidationError('Name doesnt exist on user element')
        if type(user.get('name')) != str:
            raise serializers.ValidationError('Name is not a string')
        if self.context.get('user').username == user.get('name'):
            raise serializers.ValidationError('User can not be same as owner')

    def check_permissions(self, user):
        if 'permissions' not in user:
            raise serializers.ValidationError('Permissions doesnt exist on user element')

        permissions = user.get('permissions')
        if type(permissions) != list:
            raise serializers.ValidationError('Permissions is not a list')
        for permission in permissions:
            self.check_permission(permission)

    @staticmethod
    def check_permission(permission):
        if permission not in [READ, WRITE, DELETE]:
            raise serializers.ValidationError('Permission is not in RD, WT, DE')

    def validate_users(self, users):
        users_name = []
        for user in users:
            self.check_name(user)
            self.check_permissions(user)
            if user.get('name', '') in users_name:
                raise serializers.ValidationError('Cannot repeat users')
            users_name.append(user.get('name'))
        if User.objects.filter(
                username__in=users_name
        ).count() != len(users_name):
            raise serializers.ValidationError('Any of user given does not exist')
        return users

    def validate(self, attrs):
        if self.context.get('user') != self.context.get('board').owner:
            raise serializers.ValidationError('Only onwer can add users')
        return attrs

    def create(self, validated_data):
        board_instance = self.context.get('board')
        users = validated_data.get('users')
        UserBoardPermissions.objects.set_user_permission_diff(users, board_instance)
        # UserBoardPermissions.objects.remove_board_users_permissions(
        #     board_instance,
        #     users,
        #     permissions
        # )
        #
        # UserBoardPermissions.objects.bulk_create(
        #     [
        #         UserBoardPermissions(
        #             user=user,
        #             board=board_instance,
        #             permission=permission
        #         )
        #         for user in validated_data.get('users')
        #         for permission in validated_data.get('permissions')
        #     ]
        # )
        return self.get_initial()

    def remove_board_users_permissions(self,):
        UserBoardPermissions.objects.remove_board_users_permissions(
            self.context.get('board'),
            self.validated_data.get('users'),
            self.validated_data.get('permissions')
        )

    class Meta:
        model = UserBoardPermissions
        fields = ('id', 'users')
        read_only_fields = (
            'id',
        )
