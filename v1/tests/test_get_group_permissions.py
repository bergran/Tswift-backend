# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions, READ, WRITE, DELETE
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions


class BoardTestListPermissions(APITestCase):
    def setUp(self):
        # Create some users
        self.user1 = User.objects.create(username='Pepito')
        self.user2 = User.objects.create(username='Benito')
        self.user3 = User.objects.create(username='Menganito')

        # Create some groups
        self.group1 = Group.objects.create(name='group 1')
        self.group1.user_set.add(self.user1)

        self.group2 = Group.objects.create(name='group 2')
        self.group2.user_set.add(self.user1)
        self.group2.user_set.add(self.user2)

        self.group3 = Group.objects.create(name='group 3')
        self.group3.user_set.add(self.user1)
        self.group3.user_set.add(self.user3)

        # Create permissions
        self.write = Permissions.objects.create(name=WRITE)
        self.read = Permissions.objects.create(name=READ)
        self.delete = Permissions.objects.create(name=DELETE)

        # Create some Boards
        self.board1 = Boards.objects.create(name='board 1', owner=self.user1)
        self.board2 = Boards.objects.create(name='board 2', owner=self.user2)
        self.board3 = Boards.objects.create(name='board 3', owner=self.user3)
        self.board4 = Boards.objects.create(name='board 4', owner=self.user3)
        self.board5 = Boards.objects.create(name='board 5', owner=self.user2)

        # Add permissions to groups
        self.relation_group_1 = GroupBoardPermissions.objects.create(
            group=self.group1,
            permission=self.read,
            board=self.board1
        )
        self.relation_group_2 = GroupBoardPermissions.objects.create(
            group=self.group2,
            permission=self.read,
            board=self.board2
        )
        self.relation_group_3 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board3
        )
        self.relation_group_4 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board4
        )

        # Add permissions to users
        self.relation_user_1 = UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.write,
            board=self.board2
        )
        self.relation_user_2 = UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.read,
            board=self.board2
        )
        self.relation_user_3 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board3
        )

    def send_request_with_authenticate(self, user, pk):
        self.client.force_login(user=user)
        response =  self.client.get('/api/v1/boards/{}/get_groups/'.format(pk))
        self.client.logout()
        return response

    def send_request_without_authenticate(self, pk):
        return self.client.get('/api/v1/boards/{}/get_groups/'.format(pk))

    def test_anonimous_user_no_boards(self):
        response = self.send_request_without_authenticate(self.board1.pk)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_board2_users(self):
        # Create response
        response = self.send_request_with_authenticate(self.user1, self.board2.pk)

        # Check response status code == 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response has 4 boards
        self.assertEqual(response.data.get('count'), 1)

    def test_get_board3_users(self):
        # Create response
        response = self.send_request_with_authenticate(self.user1, self.board3.pk)

        # Check response status code == 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response has 4 boards
        self.assertEqual(response.data.get('count'), 1)

    def test_get_board_5_users(self):
        # Create response
        response = self.send_request_with_authenticate(self.user1, self.board5.pk)

        # Check response status code == 200
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
