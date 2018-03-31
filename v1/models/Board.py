# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models

from v1.models.Permissions import READ


class BoardManager(models.Manager):
    def get_boards_access(self, user, permissions):
        return self.filter(
            models.Q(owner=user) |
            models.Q(userboardpermissions__user=user, userboardpermissions__permission__name__in=permissions) |
            models.Q(
                groupboardpermissions__group__in=user.groups.all(),
                groupboardpermissions__permission__name__in=permissions)
        ).distinct()

    def has_boards_access(self, user, board_instance, permissions=[READ]):
        return self.get_boards_access(user, permissions).filter(
            pk=board_instance.pk
        ).exists()


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
