# -*- coding: utf-8 -*-

from django.db import models


class GroupBoardPermissionManager(models.Manager):
    def remove_board_groups_permissions(self, board, groups, permissions):
        self.filter(
            board=board,
            group__in=groups,
            permission__in=permissions
        ).delete()


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
