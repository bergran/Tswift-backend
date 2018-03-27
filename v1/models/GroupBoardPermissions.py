# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models

from v1.models.Permissions import Permissions
from v1.models.Board import Boards


class GroupBoardPermissionManager(models.Manager):
    def remove_board_groups_permissions(self, board, groups, permissions):
        self.filter(
            board=board,
            group__in=groups,
            permission__in=permissions
        ).delete()


class GroupBoardPermissions(models.Model):
    group = models.ForeignKey(django_models.Group,
                              on_delete=models.CASCADE
                              )
    board = models.ForeignKey(Boards,
                              on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions,
                                   on_delete=models.CASCADE,
                                   )
    date_created = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = GroupBoardPermissionManager()

    class Meta:
        db_table = 'GroupBoardPermissions'
        unique_together = (('group', 'board', 'permission'), )
