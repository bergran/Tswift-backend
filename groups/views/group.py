# -*- coding: utf-8 -*-

from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from groups.filters.groups import GroupFilter
from groups.models.group_profile import Group
from groups.serializers.group_serializer import GroupProfileSerializer


class GroupsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_class = GroupFilter

    def get_queryset(self):
        return Group.objects.filter(
            models.Q(pk__in=self.request.user.groups.all()) |
            models.Q(profile__owner=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        return GroupProfileSerializer

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }
