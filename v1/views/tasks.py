# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from v1.models.Task import Tasks
from v1.models.Board import Boards
from v1.serializers.tasks.serializer import TasksSerializer
from v1.permissions.tasks.permissions import TasksPermissions


class TasksViewset(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Tasks.objects.all()
    permission_classes = (IsAuthenticated, TasksPermissions)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        # To show tasks that are owner, has access by group or user
        return queryset.filter(
            board__in=Boards.permissions.get_boards_access(
                user,
                ['read']
            )
        )

    def get_serializer_class(self):
        return TasksSerializer

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
