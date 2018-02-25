# -*- coding: utf-8 -*-

from django.db import models

from v1.models.Board import Boards
from v1.models.State import States


class Tasks(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_expired = models.DateTimeField(null=True, default=None)
    deleted = models.BooleanField(default=False)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    board = models.ForeignKey(Boards, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Tasks'
        ordering = ['-date_created']
