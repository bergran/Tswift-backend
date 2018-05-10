# -*- coding: utf-8 -*-


from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.filters.board_filter import BoardFilters
from v1.models import UserBoardPermissions, GroupBoardPermissions
from v1.models.Board import Boards
from v1.models.Permissions import READ
from v1.permissions.boards.permission import BoardPermission
from v1.serializers.boards.get_groups import BoardPermissionsGroups
from v1.serializers.boards.get_users import BoardPermissions
from v1.serializers.boards.serializer import BoardSerializer
from v1.serializers.boards.serializer_list import BoardListSerializer
from v1.serializers.boards.change_name import ChangeNameSerializer
from v1.serializers.boards.add_users import BoardAddUserSerializer
from v1.serializers.boards.add_groups import BoardAddGroupSerializer
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

            return Boards.permissions.get_boards_access(
                self.request.user,
                [READ]
            )
        return queryset

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_users_groups(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs.get('context').update({'board': self.get_object()})
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'change_name':
            return ChangeNameSerializer
        elif self.action == 'list':
            return BoardListSerializer
        elif self.action == 'get_states':
            return GetStatesSerializer
        elif self.action == 'set_user_permissions':
            return BoardAddUserSerializer
        elif self.action == 'set_group_permissions':
            return BoardAddGroupSerializer
        elif self.action in ['get_user_boards']:
            return BoardPermissions
        elif self.action in ['get_groups_board']:
            return BoardPermissionsGroups
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

    @detail_route(['get'], url_path='states')
    def get_states(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='set-user-permissions')
    def set_user_permissions(self, request, *args, **kwargs):
        serializer = self.get_serializer_users_groups(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_set_users_permissions(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @detail_route(methods=['post'], url_path='set-group-permissions')
    def set_group_permissions(self, request, *args, **kwargs):
        serializer = self.get_serializer_users_groups(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_set_groups_permissions(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @detail_route(methods=['get'], url_path='get_users')
    def get_user_boards(self, request, pk, *args, **kwargs):
        obj = self.get_object()
        users = UserBoardPermissions.objects.get_boards_users(obj)

        page = self.paginate_queryset(users)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(data=serializer.data)

    @detail_route(methods=['get'], url_path='get_groups')
    def get_groups_board(self, request, pk, *args, **kwargs):
        obj = self.get_object()
        groups = GroupBoardPermissions.objects.get_boards_groups(obj)

        page = self.paginate_queryset(groups)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(groups, many=True)
        return Response(data=serializer.data)

    @staticmethod
    def perform_destroy(instance):
        instance.deleted = True
        instance.save()

    @staticmethod
    def perform_set_users_permissions(serializer):
        serializer.save()\

    @staticmethod
    def perform_set_groups_permissions(serializer):
        serializer.save()

    @staticmethod
    def perform_add_groups(serializer):
        serializer.save()
