# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models


class BoardManager(models.Manager):
    def get_boards_access(self, user):
        return self.filter(
            Q(owner=user) |
            Q(userboardpermissions__user=user, userboardpermissions__permission__name='read') |
            Q(groupboardpermissions__group__in=user.groups.all(), groupboardpermissions__permission__name='read')
        ).distinct()


class Boards(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(django_models.User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    # Managers
    permissions = BoardManager()
    objects = models.Manager()

    class Meta:
        db_table = 'Boards'
        unique_together = (('name', 'owner'), )
        ordering = ('date_created',)
