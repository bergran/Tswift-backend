# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models import UserBoardPermissions
from v1.models.Board import Boards
from v1.models.Permissions import Permissions, READ, WRITE, DELETE


class StatesTestRetrieve(APITestCase):
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
            user=self.user1,
            permission=self.read,
            board=self.board2
        )

        self.user_permission_1 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board1
        )

        self.user_permission_2 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.write,
            board=self.board1
        )
        self.user_permission_3 = UserBoardPermissions.objects.create(
            user=self.user3,
            permission=self.read,
            board=self.board1
        )
        self.user_permission_4 = UserBoardPermissions.objects.create(
            user=self.user3,
            permission=self.write,
            board=self.board1
        )

        self.user_permission_5 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.delete,
            board=self.board1
        )

        self.user_permission_6 = UserBoardPermissions.objects.create(
            user=self.user3,
            permission=self.delete,
            board=self.board1
        )


    def get_uri(self, pk):
        return '/api/v1/boards/{}/delete_users/'.format(pk)

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
            'users': [self.user2.username, self.user3.username],
            'permissions': [self.write.name, self.read.name]

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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(UserBoardPermissions.objects.filter(
            pk__in=[
                self.user_permission_1.pk,
                self.user_permission_2.pk,
                self.user_permission_3.pk,
                self.user_permission_4.pk
            ]
        ).exists())

        self.assertTrue(UserBoardPermissions.objects.filter(
            pk__in=[
                self.user_permission_5.pk,
                self.user_permission_6.pk
            ]
        ).exists())

    def check_serializer_fields(self, payload):
        self.assertIn('users', payload)
        self.assertIn('permissions', payload)

    def test_add_users_successfully(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [self.user2.username, self.user3.username],
            'permissions': [self.write.name, self.read.name]

        }

        # launch tests
        self.launch_test_successfully(user, board, params)

    def test_add_users_can_not_add_self_user(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [self.user1.username, self.user2.username, self.user3.username],
            'permissions': [self.write.name, self.read.name]

        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            board.pk,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check can not add same user
        self.assertIn('users', response.data)

    def test_add_users_can_not_add_duplicate_users(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [self.user2.username, self.user2.username, self.user3.username],
            'permissions': [self.write.name, self.read.name]

        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            board.pk,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check can not add same user
        self.assertIn('users', response.data)

    def test_add_users_no_permissions(self):
        # params
        user = self.user1
        board = self.board1
        params = {
            'users': [self.user2.username, self.user3.username],
            'permissions': []

        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            board.pk,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check can not add same user
        self.assertIn('permissions', response.data)

    def test_add_users_only_owner_can_add_user(self):
        # params
        user = self.user1
        board = self.board2
        params = {
            'users': [self.user2.username, self.user3.username],
            'permissions': [self.write.name, self.read.name]

        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            board.pk,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check can not add same user
        self.assertIn('non_field_errors', response.data)
