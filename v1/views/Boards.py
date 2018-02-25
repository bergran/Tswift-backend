# -*- coding: utf-8 -*-

from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.filters.board_filter import BoardFilters
from v1.models.Board import Boards
from v1.permissions.boards.permission import BoardPermission
from v1.serializers.boards.serializer import BoardSerializer
from v1.serializers.boards.serializer_list import BoardListSerializer
from v1.serializers.boards.change_name import ChangeNameSerializer
from v1.serializers.boards.get_states import GetStatesSerializer


class BoardView(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Boards.objects.all()
    permission_classes = [IsAuthenticated, BoardPermission]
    serializer_class = BoardSerializer
    filter_class = BoardFilters

    def get_queryset(self):
        queryset = self.queryset
        if self.action not in [
            'destroy',
            'retrieve',
            'change_name',
            'get_states'
        ]:
            user = self.request.user

            return queryset.filter(
                Q(owner=user) |
                Q(userboardpermissions__user=user, userboardpermissions__permission__name='read') |
                Q(groupboardpermissions__group__in=user.groups.all(), groupboardpermissions__permission__name='read')
            ).distinct()
        return queryset

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_class(self):
        if self.action == 'change_name':
            return ChangeNameSerializer
        elif self.action == 'list':
            return BoardListSerializer
        elif self.action == 'get_states':
            return GetStatesSerializer
        else:
            return BoardSerializer

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated, BoardPermission])
    def change_name(self, request, pk=None):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            instance.name = serializer.data.get('name')
            instance.save()
            return Response(BoardSerializer(instance).data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(['get'])
    def get_states(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

