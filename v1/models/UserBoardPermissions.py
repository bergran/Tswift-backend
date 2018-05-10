# -*- coding: utf-8 -*-

from django.contrib.auth import models as django_models
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from v1.models.Permissions import Permissions
from v1.models.Board import Boards


class UserBoardPermissionManager(models.Manager):
    def remove_board_users_permissions(self, board, users, permissions):
        return self.filter(
            board=board,
            user__in=users,
            permission__in=permissions
        ).delete()

    def get_boards_users(self, board):
        return self.filter(board=board)

    def set_user_permission_diff(self, users, board):
        user_filter_exclude = Q()

        users_name = []
        for user in users:
            user_name = user.get('name', '')
            user_filter_exclude |= Q(
                user__username=user_name,
                board=board,
                permission__name__in=user.get('permissions', [])
            )
            users_name.append(user_name)

        created_previously = self.filter(
            user_filter_exclude
        ).values('user__username', 'permission__name')

        self.exclude(user_filter_exclude).filter(
            user__username__in=users_name, board=board
        ).delete()

        return self.bulk_create(
            [
                UserBoardPermissions(
                    user=User.objects.get(username=user.get('name')),
                    permission=Permissions.objects.get(name=permission),
                    board=board
                ) for user in users
                for permission in user.get('permissions')
                if {
                    'user__username': user.get('name'),
                    'permission__name': permission
                } not in created_previously
            ]
        )


class UserBoardPermissions(models.Model):
    user = models.ForeignKey(
        django_models.User,
        on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        Boards,
        on_delete=models.CASCADE
    )
    permission = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = UserBoardPermissionManager()

    class Meta:
        db_table = 'UserBoardPermissions'
        unique_together = (('user', 'board', 'permission'), )
        ordering = ('pk', )
