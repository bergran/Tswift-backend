# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from v1.models.Permissions import READ, WRITE, DELETE


class PermissionView(
    GenericViewSet,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticated, ]
    queryset = None

    def get_serializer_class(self):
        return None

    def list(self, request, *args, **kwargs):
        return Response({
            'read': READ,
            'write': WRITE,
            'delete': DELETE
        })
