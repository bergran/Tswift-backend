# -*- coding: utf-8 -*-

from django.db import models

READ = 'RD'
WRITE = 'WT'
DELETE = 'DE'


class PermissionManager(models.Manager):
    def get_permissions(self, permissions):
        if set([READ, WRITE, DELETE]).issubset(permissions):
            return self.none()
        return self.filter(
            name__in=permissions
        )


class Permissions(models.Model):
    names = (
        (READ, 'Read'),
        (WRITE, 'Write'),
        (DELETE, 'Delete')
    )
    users = models.ManyToManyField(
        'auth.User',
        through='UserBoardPermissions',
        through_fields=('permission', 'user'),
        related_name='users_custom'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        through='GroupBoardPermissions',
        through_fields=('permission', 'group'),
        related_name='groups_custom'
    )

    name = models.CharField(max_length=20, choices=names)

    # Managers
    permissions = PermissionManager()
    objects = models.Manager()

    class Meta:
        db_table = 'Permissions'
