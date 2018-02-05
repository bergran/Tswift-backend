# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import models as django_models


class Permissions(models.Model):
    READ = 'RD'
    WRITE = 'WT'
    DELETE = 'DE'
    names = (
        (READ, 'Read'),
        (WRITE, 'Write'),
        (DELETE, 'Delete')
    )
    users = models.ManyToManyField(
        django_models.User,
        through='UserBoardPermissions',
        through_fields=('permission', 'user'),
        related_name='users_custom'
    )
    groups = models.ManyToManyField(
        django_models.Group,
        through='GroupBoardPermissions',
        through_fields=('permission', 'group'),
        related_name='groups_custom'
    )

    name = models.CharField(max_length=20, choices=names)

    class Meta:
        db_table = 'Permissions'
