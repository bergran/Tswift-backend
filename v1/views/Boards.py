# -*- coding: utf-8 -*-

from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from v1.filters.board_filter import BoardFilters
from v1.models.Board import Boards
from v1.permissions.boards.permission import BoardPermission
from v1.serializers.boards.serializer import BoardSerializer
from v1.serializers.boards.change_name import ChangeNameSerializer


class BoardView(ModelViewSet):
    queryset = Boards.objects.all()
    permission_classes = [IsAuthenticated, BoardPermission]
    serializer_class = BoardSerializer
    filter_class = BoardFilters

    def get_queryset(self):
        user = self.request.user
        return Boards.objects.filter(
            Q(owner=self.request.user) | Q(userboardpermissions__user=user) |
            Q(groupboardpermissions__group__in=user.groups.all())
        )

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_serializer_class(self):
        if self.action == 'change_name':
            return ChangeNameSerializer
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
        pass
