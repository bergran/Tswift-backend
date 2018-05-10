# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from rest_framework import serializers

from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.models.Permissions import READ, WRITE, DELETE, Permissions


class BoardAddGroupSerializer(serializers.ModelSerializer):
    groups = serializers.ListField(
        child=serializers.JSONField(),
        help_text='Users nickname that you want to invite to the board'
    )

    def check_name(self, group):
        if 'name' not in group:
            raise serializers.ValidationError('Name doesnt exist on group element')
        if type(group.get('name')) != str:
            raise serializers.ValidationError('Name is not a string')

    def check_permissions(self, group):
        if 'permissions' not in group:
            raise serializers.ValidationError('Permissions doesnt exist on user element')

        permissions = group.get('permissions')
        if type(permissions) != list:
            raise serializers.ValidationError('Permissions is not a list')
        for permission in permissions:
            self.check_permission(permission)

    @staticmethod
    def check_permission(permission):
        if permission not in [READ, WRITE, DELETE]:
            raise serializers.ValidationError('Permission is not in RD, WT, DE')

    def validate_groups(self, groups):
        groups_name = []
        for group in groups:
            self.check_name(group)
            self.check_permissions(group)
            if group.get('name', '') in groups_name:
                raise serializers.ValidationError('Cannot repeat users')
            groups_name.append(group.get('name'))
        if Group.objects.filter(
                name__in=groups_name
        ).count() != len(groups_name):
            raise serializers.ValidationError('Any of groups given does not exist')
        return groups

    def validate(self, attrs):
        user = self.context.get('user')
        board = self.context.get('board')

        if board.owner != user:
            raise serializers.ValidationError('User is not the owner')

        return attrs

    def create(self, validated_data):
        groups = validated_data.get('groups')
        board = self.context.get('board')
        GroupBoardPermissions.objects.set_groups_permission_diff(
            groups,
            board
        )
        #
        # GroupBoardPermissions.objects.bulk_create(
        #     [
        #         GroupBoardPermissions(
        #             group=group,
        #             permission=permission,
        #             board=board
        #         )
        #         for group in groups
        #         for permission in permissions
        #     ]
        # )
        # return {
        #     'groups': groups,
        #     'permissions': self.get_initial().get('permissions')
        # }
        return self.get_initial()


    def remove_board_groups_permissions(self):
        GroupBoardPermissions.objects.remove_board_groups_permissions(
            self.context.get('board'),
            self.validated_data.get('groups'),
            self.validated_data.get('permissions')
        )

    class Meta:
        model = GroupBoardPermissions
        fields = ('groups', )
