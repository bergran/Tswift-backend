# -*- coding: utf-8 -*-

from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.models.State import States


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
            permission=self.read,
            board=self.board1
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

    def get_uri(self, pk):
        return '/api/v1/states/{}/'.format(pk)

    def send_request_with_authenticate(self, user, pk):
        # Get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.get(uri)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, pk):
        # Get uri
        uri = self.get_uri(pk)

        # Send request and return it
        return self.client.get(uri)

    def test_anonimous_user_no_states(self):
        response = self.send_request_without_authenticate(self.board1.pk)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def launch_test_successfully(self, user, state):
        # Send request
        response = self.send_request_with_authenticate(
            user,
            state.pk
        )

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializers fields are on payload
        self.assertIn('id', payload)
        self.assertIn('name', payload)
        self.assertIn('date_created', payload)
        self.assertIn('date_modified', payload)
        self.assertIn('deleted', payload)

        # Check data
        self.assertEqual(payload.get('id'), state.pk)
        self.assertEqual(payload.get('name'), state.name)
        self.assertEqual(parse_datetime(
            payload.get('date_created')),
            state.date_created
        )
        self.assertEqual(parse_datetime(
            payload.get('date_modified')),
            state.date_modified
        )
        self.assertEqual(payload.get('deleted'), state.deleted)

    def test_list_status_state_1_user1(self):
        # Params
        user = self.user1
        state = self.state1

        self.launch_test_successfully(user, state)

    def test_list_status_state_2_user1(self):
        # Params
        user = self.user1
        state = self.state2

        self.launch_test_successfully(user, state)

    def test_list_status_state_3_user2(self):
        # Params
        user = self.user2
        state = self.state3

        self.launch_test_successfully(user, state)

    def test_list_status_board_3_user2(self):
        # Params
        user = self.user2
        state = self.state3

        self.launch_test_successfully(user, state)

    def test_list_status_board_1_user2_forbidden(self):
        # Params
        user = self.user2
        board = self.board1

        # Send request
        response = self.send_request_with_authenticate(user, board.pk)

        # Check response status code is equals to 403
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
