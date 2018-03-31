# -*- coding: utf-8 -*-

from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from groups.filters.groups import GroupFilter
from groups.models.group_profile import Group
from groups.permissions.owner_permissions import OwnerPermission
from groups.serializers.group_serializer import GroupProfileSerializer
from groups.serializers.group_users_serializer import GroupUserSerializer


class GroupsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, OwnerPermission]
    filter_class = GroupFilter

    def get_queryset(self):
        return Group.objects.filter(
            models.Q(pk__in=self.request.user.groups.all()) |
            models.Q(profile__owner=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.action in [
            'add_users',
            'delete_users'
        ]:
            return GroupUserSerializer
        else:
            return GroupProfileSerializer

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_users(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['context'].update({
            'group': self.get_object(),
            'action': self.action
        })
        return serializer_class(*args, **kwargs)

    @detail_route(methods=['post'], url_path='add_users')
    def add_users(self, request, *args, **kwargs):
        serializer = self.get_serializer_users(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_add_users(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='delete_users')
    def delete_users(self, request, *args, **kwargs):
        serializer = self.get_serializer_users(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_delete_users(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_add_users(self, serializer):
        serializer.save()

    def perform_delete_users(self, serializer):
        serializer.remove_users()
