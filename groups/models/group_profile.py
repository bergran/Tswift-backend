# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group, User
from django.db import models


class GroupProfileManager(models.Manager):
    def create_group(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        group = Group.objects.create(*args, **kwargs)
        self.create(group=group, owner=owner)
        return group


class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='profile')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Manager
    objects = GroupProfileManager()


@property
def owner(self):
    return self.profile.owner if self.profile else None


Group.owner = owner
