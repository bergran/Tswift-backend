# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q

from v1.models import Permissions


class GroupBoardPermissionManager(models.Manager):
    def remove_board_groups_permissions(self, board, groups, permissions):
        self.filter(
            board=board,
            group__in=groups,
            permission__in=permissions
        ).delete()

    def get_boards_groups(self, board):
        return self.filter(board=board)

    def set_groups_permission_diff(self, groups, board):
        group_filter_exclude = Q()

        groups_name = []
        for group in groups:
            group_name = group.get('name', '')
            group_filter_exclude |= Q(
                group__name=group_name,
                board=board,
                permission__name__in=group.get('permissions', [])
            )
            groups_name.append(group_name)

        created_previously = self.filter(
            group_filter_exclude
        ).values('group__name', 'permission__name')

        self.exclude(group_filter_exclude).filter(
            group__name__in=groups_name, board=board
        ).delete()

        return self.bulk_create(
            [
                GroupBoardPermissions(
                    group=Group.objects.get(name=group.get('name')),
                    permission=Permissions.objects.get(name=permission),
                    board=board
                ) for group in groups
                for permission in group.get('permissions')
                if {
                    'group__name': group.get('name'),
                    'permission__name': permission
                } not in created_previously
            ]
        )


class GroupBoardPermissions(models.Model):
    group = models.ForeignKey('auth.Group',
                              on_delete=models.CASCADE
                              )
    board = models.ForeignKey('v1.Boards',
                              on_delete=models.CASCADE)
    permission = models.ForeignKey('v1.Permissions',
                                   on_delete=models.CASCADE,
                                   )
    date_created = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = GroupBoardPermissionManager()

    class Meta:
        db_table = 'GroupBoardPermissions'
        unique_together = (('group', 'board', 'permission'), )
        ordering = ('id', )
