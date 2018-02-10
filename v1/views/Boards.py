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
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.Permissions import Permissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.permissions.boards.permission import BoardPermission
from v1.serializers.boards.serializer import BoardSerializer
from v1.serializers.boards.serializer_list import BoardListSerializer
from v1.serializers.boards.change_name import ChangeNameSerializer


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
        user = self.request.user
        try:
            read_permission = Permissions.objects.get(name='read')
        except Permissions.DoesNotExist:
            return Boards.objects.none()

        user_permissions_board = UserBoardPermissions.objects.filter(user=user, permission=read_permission)
        groups_permissions_board = GroupBoardPermissions.objects.filter(group__in=user.groups.all(), permission=read_permission)
        return Boards.objects.filter(
            Q(owner=self.request.user) |
            Q(userboardpermissions__in=user_permissions_board) |
            Q(groupboardpermissions__in=groups_permissions_board)
        )

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_class(self):
        if self.action == 'change_name':
            return ChangeNameSerializer
        elif self.action == 'list':
            return BoardListSerializer
        else:
            return BoardSerializer

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated, BoardPermission])
    def change_name(self, request, pk=None):
        try:
            instance = Boards.objects.get(pk=pk)
        except Boards.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            instance.name = serializer.data.get('name')
            instance.save()
            return Response(BoardSerializer(instance).data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

