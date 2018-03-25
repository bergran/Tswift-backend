# -*- coding: utf-8 -*-

from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.models.State import States
from v1.models.Task import Tasks


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
        self.write = Permissions.objects.create(name='write')
        self.read = Permissions.objects.create(name='read')
        self.delete = Permissions.objects.create(name='delete')

        # Create some Boards
        self.board1 = Boards.objects.create(name='board 1', owner=self.user1)
        self.board2 = Boards.objects.create(name='board 2', owner=self.user2)
        self.board3 = Boards.objects.create(name='board 3', owner=self.user3)
        self.board4 = Boards.objects.create(name='board 4', owner=self.user3)

        # Create states
        self.state1 = States.objects.create(name='state 1', board=self.board1)
        self.state2 = States.objects.create(name='state 2', board=self.board1)
        self.state3 = States.objects.create(name='state 3', board=self.board2)
        self.state4 = States.objects.create(name='state 4', board=self.board2)
        self.state5 = States.objects.create(name='state 5', board=self.board2)
        self.state6 = States.objects.create(name='state 6', board=self.board3)

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
            permission=self.delete,
            board=self.board2
        )
        self.relation_group_3 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board3
        )
        GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.delete,
            board=self.board3
        )
        self.relation_group_4 = GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.read,
            board=self.board4
        )
        GroupBoardPermissions.objects.create(
            group=self.group3,
            permission=self.delete,
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
            permission=self.delete,
            board=self.board2
        )
        self.relation_user_3 = UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.read,
            board=self.board3
        )
        UserBoardPermissions.objects.create(
            user=self.user2,
            permission=self.delete,
            board=self.board3
        )

    def get_uri(self):
        return '/api/v1/tasks/'

    def send_request_with_authenticate(self, user, params):
        # Get uri
        uri = self.get_uri()

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.post(uri, params)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, params):
        # Get uri
        uri = self.get_uri()

        # Send request and return it
        return self.client.post(uri, params)

    def test_anonimous_user_no_states(self):
        params = {
            'title': 'Tasks 1',
            'description': 'Some description',

        }
        response = self.send_request_without_authenticate(params)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def launch_test_successfully(self, user, params):
        # Send request
        response = self.send_request_with_authenticate(
            user,
            params
        )

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.data
        # Check serializers fields are on payload results
        self.assertIn('id', payload)
        self.assertIn('title', payload)
        self.assertIn('description', payload)
        self.assertIn('date_created', payload)
        self.assertIn('date_modified', payload)
        self.assertIn('date_expired', payload)
        self.assertIn('deleted', payload)
        self.assertIn('state', payload)
        self.assertIn('board', payload)

    def test_create_tasks(self):
        # params
        user = self.user1
        params = {
            'title': 'Tasks 1',
            'description': 'Some description',
            'board': self.board1.pk,
            'state': self.state1.pk
        }

        # launch tests
        self.launch_test_successfully(user, params)

    def test_create_tasks_state_not_in_board(self):
        # params
        user = self.user1
        params = {
            'title': 'Tasks 1',
            'description': 'Some description',
            'board': self.board2.pk,
            'state': self.state1.pk
        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tasks_no_board_access(self):
        # params
        user = self.user2
        params = {
            'title': 'Tasks 1',
            'description': 'Some description',
            'board': self.board1.pk,
            'state': self.state1.pk
        }

        # Send request
        response = self.send_request_with_authenticate(
            user,
            params
        )

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)