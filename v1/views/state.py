# -*- coding: utf-8 -*-

from django.db.models import Q

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


from v1.models.State import States
from v1.serializers.tasks_states.serializer import StateSerializer
from v1.permissions.states.permissions import StatesPermission


class StatesView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    queryset = States.objects.all()
    permission_classes = [IsAuthenticated, StatesPermission]

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_class(self):
        if self.action == 'get_tasks':
            return StateSerializer
        else:
            return StateSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        return queryset.filter(
            Q(board__owner=user) |
            Q(board__userboardpermissions__user=user, board__userboardpermissions__permission__name='read') |
            Q(board__groupboardpermissions__group__in=user.groups.all(), board__groupboardpermissions__permission__name='read')
        ).distinct()
        return queryset

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
