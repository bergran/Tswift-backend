# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models

from v1.models.Permissions import Permissions
from v1.models.Board import Boards


class UserBoardPermissions(models.Model):
    user = models.ForeignKey(django_models.User,
                             on_delete=models.CASCADE)
    board = models.ForeignKey(Boards,
                              on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions,
                                    on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserBoardPermissions'
        unique_together = (('user', 'board', 'permission'), )
