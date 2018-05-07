# -*- coding: utf-8 -*-

from django.utils import timezone
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions, READ, WRITE, DELETE
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
        self.write = Permissions.objects.create(name=WRITE)
        self.read = Permissions.objects.create(name=READ)
        self.delete = Permissions.objects.create(name=DELETE)

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

        self.task1 = Tasks.objects.create(
            title='task 1',
            description='Some description',
            date_expired=timezone.now() + timezone.timedelta(days=1),
            state=self.state1,
            board=self.state1.board
        )
        self.task2 = Tasks.objects.create(
            title='task 2',
            description='Some description',
            date_expired=timezone.now() + timezone.timedelta(hours=5),
            state=self.state1,
            board=self.state1.board
        )
        self.task3 = Tasks.objects.create(
            title='task 3',
            description='Some description',
            date_expired=timezone.now() - timezone.timedelta(minutes=5),
            state=self.state1,
            board=self.state1.board
        )

        self.task4 = Tasks.objects.create(
            title='task 4',
            description='Some description',
            date_expired=timezone.now(),
            state=self.state2,
            board=self.state2.board
        )
        self.task5 = Tasks.objects.create(
            title='task 5',
            description='Some description',
            date_expired=timezone.now(),
            state=self.state2,
            board=self.state2.board
        )
        self.task6 = Tasks.objects.create(
            title='task 6',
            description='Some description',
            date_expired=timezone.now(),
            state=self.state2,
            board=self.state2.board
        )

    def get_uri(self, pk):
        return '/api/v1/states/{}/tasks/'.format(pk)

    def send_request_with_authenticate(self, user, pk, params):
        # Get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.get(uri, params)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, pk, params):
        # Get uri
        uri = self.get_uri(pk)

        # Send request and return it
        return self.client.get(uri, params)

    def test_anonimous_user_no_states(self):
        params = {}
        response = self.send_request_without_authenticate(self.board1.pk, params)

        # Check status code is == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def launch_test_successfully(self, user, state, tasks_length, params):
        # Send request
        response = self.send_request_with_authenticate(
            user,
            state.pk,
            params
        )

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check length is equals to length_param
        self.assertEqual(len(payload), tasks_length)

    def test_get_tasks_status_state_1_user1(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 3
        params = {}

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_status_state_2_user1(self):
        # Params
        user = self.user1
        state = self.state2
        tasks = 3
        params = {}

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_status_state_3_user2(self):
        # Params
        user = self.user2
        state = self.state3
        tasks = 0
        params = {}

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_status_state_6_user2(self):
        # Params
        user = self.user2
        state = self.state6
        tasks = 0
        params = {}

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_status_board_1_user2_forbidden(self):
        # Params
        user = self.user2
        board = self.board1
        params = {
            'title': self.task1.title
        }

        # Send request
        response = self.send_request_with_authenticate(user, board.pk, params)

        # Check response status code is equals to 403
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_tasks_filtering_by_title(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 1
        params = {
            'title': self.task1.title
        }

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_filtering_by_date_create_range(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 3
        params = {
            'start_date': self.task1.date_created,
            'end_date': self.task3.date_created
        }

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_filtering_by_is_expired_true(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 1
        params = {
            'is_expired': True
        }

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_filtering_by_is_expired_false(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 2
        params = {
            'is_expired': False
        }

        self.launch_test_successfully(user, state, tasks, params)

    def test_get_tasks_filtering_by_title_contains(self):
        # Params
        user = self.user1
        state = self.state1
        tasks = 3
        params = {
            'title': 'task'
        }

        self.launch_test_successfully(user, state, tasks, params)
