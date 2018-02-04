# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models

from v1.models.Permissions import Permissions
from v1.models.Board import Boards


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

    class Meta:
        db_table = 'GroupBoardPermissions'
        unique_together = (('group', 'board', 'permission'), )
