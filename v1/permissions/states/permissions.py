# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

from v1.models.Board import Boards

class StatesPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in [
            'get_tasks',
            'retrieve',
        ]:
            permissions_name = ['read']
        elif view.action == 'destroy':
            permissions_name = ['delete', 'read']
        elif view.action in [
            'change_name',
            'create'
        ]:
            permissions_name = ['read', 'write']
        else:
            permissions_name = ['read', 'write', 'delete']

        user = request.user
        return Boards.permissions.has_boards_access(
            user,
            obj.board,
            permissions_name
        )
