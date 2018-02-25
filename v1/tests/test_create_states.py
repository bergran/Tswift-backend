# -*- coding: utf-8 -*-

from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions


class StatesTestCreate(APITestCase):
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
        self.write = Permissions.objects.create(name='write')
        self.read = Permissions.objects.create(name='read')
        self.delete = Permissions.objects.create(name='delete')

        # Create some Boards
        self.board1 = Boards.objects.create(name='board 1', owner=self.user1)
        self.board2 = Boards.objects.create(name='board 2', owner=self.user2)
        self.board3 = Boards.objects.create(name='board 3', owner=self.user3)
        self.board4 = Boards.objects.create(name='board 4', owner=self.user3)

        # Add permissions to groups
        self.relation_group_1 = GroupBoardPermissions.objects.create(
            group=self.group1,
            permission=self.read,
            board=self.board1
        )
        GroupBoardPermissions.objects.create(
            group=self.group1,
            permission=self.write,
            board=self.board1
        )
        self.relation_group_2 = GroupBoardPermissions.objects.create(
            group=self.group2,
            permission=self.read,
            board=self.board2
        )
        GroupBoardPermissions.objects.create(
            group=self.group2,
            permission=self.write,
            board=self.board2
        )
        self.relation_group_3 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board3
        )
        GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.write,
            board=self.board3
        )
        self.relation_group_4 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board4
        )
        GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.write,
            board=self.board4
        )

        # Add permissions to users
        self.relation_user_1 = UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.read,
            board=self.board1
        )
        UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.write,
            board=self.board1
        )
        self.relation_user_2 = UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.read,
            board=self.board2
        )
        UserBoardPermissions.objects.create(
            user=self.user1,
            permission=self.write,
            board=self.board2
        )
        self.relation_user_3 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board3
        )
        UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.write,
            board=self.board3
        )

    def get_uri(self):
        return '/api/v1/states/'

    def send_request_with_authenticate(self, user, data):
        # Get uri
        uri = self.get_uri()

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.post(uri, data)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, data):
        # Get uri
        uri = self.get_uri()

        # Send request and return it
        return self.client.post(uri, data)

    def test_anonimous_user_no_states(self):
        data = {
            'name': 'state no auth',
            'board': self.board1.pk
        }
        response = self.send_request_without_authenticate(data)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def launch_test_successfully(self, user, data):
        # Send request
        response = self.send_request_with_authenticate(user, data)

        # Check response status code is equals to 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.data
        # Check serializers fields are on payload
        self.assertIn('id', payload)
        self.assertIn('name', payload)
        self.assertIn('date_created', payload)
        self.assertIn('date_modified', payload)
        self.assertIn('deleted', payload)

        # Check data
        self.assertEqual(payload.get('name'), data.get('name'))

    def test_create_state_on_board_1_user1(self):
        # Params
        user = self.user1
        data = {
            'name': 'State1',
            'board': self.board1.pk
        }

        self.launch_test_successfully(user, data)

    def test_create_state_on_board_2_user1(self):
        # Params
        user = self.user1
        data = {
            'name': 'State2',
            'board': self.board2.pk
        }

        self.launch_test_successfully(user, data)

    def test_create_state_on_board_2_user2(self):
        # Params
        user = self.user2
        data = {
            'name': 'State3',
            'board': self.board2.pk
        }

        self.launch_test_successfully(user, data)

    def test_create_state_on_board_3_user2(self):
        # Params
        user = self.user2
        data = {
            'name': 'State3',
            'board': self.board3.pk
        }

        self.launch_test_successfully(user, data)

    def test_create_status_on_board_1_user2_bad_request(self):
        # Params
        user = self.user2
        board = self.board1
        data = {
            'name': 'State 4',
            'board': board.pk
        }

        # Send request
        response = self.send_request_with_authenticate(user, data)

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
