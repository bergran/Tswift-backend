# -*- coding: utf-8 -*-

from rest_framework.permissions import BasePermission

from v1.models.Board import Boards
from v1.models.Permissions import READ, WRITE, DELETE


class BoardPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['get_states', 'retrieve']:
            permissions_name = [READ]
        elif view.action == 'destroy':
            permissions_name = [READ, DELETE]
        elif view.action in [
            'change_name',
            'create'
        ]:
            permissions_name = [READ, WRITE]
        else:
            permissions_name = [READ, WRITE, DELETE]

        user = request.user
        return Boards.permissions.has_boards_access(user, obj, permissions_name)
