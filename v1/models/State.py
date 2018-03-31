# -*- coding: utf-8 -*-

from django.db import models

from v1.models.Board import Boards


class States(models.Model):
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='states')
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'States'
        unique_together = (('name', 'board'), )
        ordering = ('date_created', )
