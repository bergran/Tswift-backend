# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models import UserBoardPermissions
from v1.models.Board import Boards
from v1.models.Permissions import Permissions, READ, WRITE, DELETE


class BoardTestSetUser(APITestCase):
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

        UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board1
        )

        UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board2
        )

        UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.delete,
            board=self.board2
        )

    def get_uri(self, pk):
        return '/api/v1/boards/{}/set-user-permissions/'.format(pk)

    def send_request_with_authenticate(self, user, pk, params):
        # Get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.post(uri, params)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, pk, params):
        # Get uri
        uri = self.get_uri(pk)

        # Send request and return it
        return self.client.post(uri, params)

    def test_anonimous_user(self):
        params = {
            'users': [
                {
                    'name': self.user2.username,
                    'permissions': [READ, WRITE]
                },
                {
                    'name': self.user3.username,
                    'permissions': [READ, DELETE]
                }
            ],
        }
        response = self.send_request_without_authenticate(self.board1, params)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def launch_test_successfully(self, user, board, params):
        # Send request
        response = self.send_request_with_authenticate(
            user,
            board.pk,
            params
        )

        # Check response status code is equals to 201
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializers fields are on payload results
        self.check_serializer_fields(payload)
        return payload

    def check_serializer_fields(self, payload):
        self.assertIn('users', payload)

    def test_set_users_successfully(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [
                {
                    'name': self.user2.username,
                    'permissions': [READ, WRITE]
                },
                {
                    'name': self.user3.username,
                    'permissions': [READ, DELETE]
                }
            ],
        }

        # launch tests
        self.launch_test_successfully(user, board, params)
        elements = UserBoardPermissions.objects.filter(
            user=self.user2,
            board=board
        )
        self.assertEqual(elements.count(), 2)

        elements = UserBoardPermissions.objects.filter(
            user=self.user3,
            board=board
        )
        self.assertEqual(elements.count(), 2)

    def test_set_users_successfully_remove_permissions_user2(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [
                {
                    'name': self.user2.username,
                    'permissions': []
                }
            ],
        }

        # launch tests
        self.launch_test_successfully(user, board, params)
        elements = UserBoardPermissions.objects.filter(
            user=self.user2,
            board=board
        )
        self.assertEqual(elements.count(), 0)

    def test_set_users_can_not_add_self_user(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [
                {
                    'name': self.user1.username,
                    'permissions': []
                }
            ],
        }

        # launch tests
        response = self.send_request_with_authenticate(user, board.pk, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_users_can_not_add_duplicate_users(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [
                {
                    'name': self.user2.username,
                    'permissions': []
                },
                {
                    'name': self.user2.username,
                    'permissions': []
                }
            ],
        }

        # launch tests
        response = self.send_request_with_authenticate(user, board.pk, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_users_only_owner_can_add_user(self):
        # params
        user = self.user2
        board = self.board1
        params = {
            'users': [
                {
                    'name': self.user2.username,
                    'permissions': []
                },
                {
                    'name': self.user3.username,
                    'permissions': []
                }
            ],
        }

        # launch tests
        response = self.send_request_with_authenticate(user, board.pk, params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
