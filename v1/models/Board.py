# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.db import models


class Boards(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(django_models.User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Boards'
        unique_together = (('name', 'owner'), )
        ordering = ('date_created',)
