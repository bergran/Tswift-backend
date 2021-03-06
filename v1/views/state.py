# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.filters.tasks_filter import TasksFilter
from v1.models import Boards
from v1.models.State import States
from v1.models.Task import Tasks
from v1.models.Permissions import READ
from v1.serializers.tasks_states.serializer import StateSerializer
from v1.serializers.tasks_states.get_tasks import GetTasksSerializer
from v1.permissions.states.permissions import StatesPermission


class StatesView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    """
        get_tasks:
            Endpoint to list a task from state <id>. You can
            paginate and filter. Query Params are:

            page (Int): page number.
            start_date(Iso_date): date where want to start lookup.
            end_date(Iso_date): date where want to end lookup.
            is_expired(Boolean): True to filter by expired or False to not.
            title(Text): lookup contains text.
    """
    queryset = States.objects.all()
    permission_classes = [IsAuthenticated, StatesPermission]

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_class(self):
        if self.action == 'get_tasks':
            return GetTasksSerializer
        else:
            return StateSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        return queryset.filter(
            board__in=Boards.permissions.get_boards_access(user, [READ])
        ).distinct()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    @detail_route(methods=['get'], url_path='tasks')
    def get_tasks(self, request, pk):
        obj = self.get_object()

        self.filter_class = TasksFilter
        queryset = Tasks.objects.filter(state=obj)

        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)

        self.filter_class = None
        return Response(serializer.data)
