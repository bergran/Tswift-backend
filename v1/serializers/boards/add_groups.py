# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from rest_framework import serializers

from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.models.Permissions import READ, WRITE, DELETE, Permissions


class BoardAddGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.MultipleChoiceField(
        choices=[
            READ,
            WRITE,
            DELETE
    ])
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )

    def validate_groups(self, groups):
        if len(set(groups)) == len(groups) and len(groups) > 0:
            return groups

        raise serializers.ValidationError('Groups are empty')

    def validate_permissions(self, permissions):
        permissions_instances = Permissions.permissions.get_permissions(permissions)
        if permissions_instances:
            return permissions_instances
        raise serializers.ValidationError('Permissions are empty')

    def validate(self, attrs):
        user = self.context.get('user')
        board = self.context.get('board')

        if board.owner != user:
            raise serializers.ValidationError('User is not the owner')

        return attrs

    def create(self, validated_data):
        groups = validated_data.get('groups')
        permissions = validated_data.get('permissions')
        board = self.context.get('board')
        GroupBoardPermissions.objects.remove_board_groups_permissions(
            board,
            groups,
            permissions
        )
        GroupBoardPermissions.objects.bulk_create(
            [
                GroupBoardPermissions(
                    group=group,
                    permission=permission,
                    board=board
                )
                for group in groups
                for permission in permissions
            ]
        )
        return {
            'groups': groups,
            'permissions': self.get_initial().get('permissions')
        }

    def remove_board_groups_permissions(self):
        GroupBoardPermissions.objects.remove_board_groups_permissions(
            self.context.get('board'),
            self.validated_data.get('groups'),
            self.validated_data.get('permissions')
        )

    class Meta:
        model = GroupBoardPermissions
        fields = ('groups', 'permissions')
