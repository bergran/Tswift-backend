# -*- coding: utf-8 -*-

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase

from v1.models.Board import Boards
from v1.models.Permissions import Permissions
from v1.models.UserBoardPermissions import UserBoardPermissions
from v1.models.GroupBoardPermissions import GroupBoardPermissions
from v1.models.State import States
from v1.models.Task import Tasks


class TasksTestPartialUpdate(APITestCase):
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
        return '/api/v1/tasks/{}/'.format(pk)

    def send_request_with_authenticate(self, user, pk, params={}):
        # Get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user=user)

        # Send request
        response = self.client.patch(uri, params)

        # Logout
        self.client.logout()

        return response

    def send_request_without_authenticate(self, pk, params={}):
        # Get uri
        uri = self.get_uri(pk)

        # Send request and return it
        return self.client.patch(uri, params)

    def launch_successfull_test(self, user, task, params):
        # Send request
        response = self.send_request_with_authenticate(user, task.pk, params)

        # Check response status code is equals to 204
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializers fields
        self.check_serializer_fields(payload)

        # Check data is same as task
        self.check_data_fields(task, payload, params)

    def check_serializer_fields(self, payload):
        self.assertIn('id', payload)
        self.assertIn('title', payload)
        self.assertIn('description', payload)
        self.assertIn('date_created', payload)
        self.assertIn('date_modified', payload)
        self.assertIn('date_expired', payload)
        self.assertIn('deleted', payload)

    def check_data_fields(self, task, payload, params):
        self.assertEqual(task.id, payload.get('id'))
        self.assertEqual(params.get('title', task.title), payload.get('title'))
        self.assertEqual(params.get('description', task.description), payload.get('description'))
        self.assertEqual(
            params.get('date_created', task.date_created),
            parse_datetime(payload.get('date_created'))
        )
        self.assertNotEqual(
            params.get('date_modified', task.date_modified),
            parse_datetime(payload.get('date_modified'))
        )
        self.assertEqual(
            params.get('date_expired', task.date_expired),
            parse_datetime(payload.get('date_expired'))
        )
        self.assertEqual(task.deleted, payload.get('deleted'))

    def test_delete_without_auth(self):
        # Send request
        response = self.send_request_without_authenticate(self.task1.pk, {
            'title': self.task1.title,
            'description': self.task1.description,
            'date_expired': self.task1.date_expired
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user1_task1(self):
        # Params
        user = self.user1
        task = self.task1
        params = {
            'title': '{}-modified'.format(task.title),
            'description': '{}-modified'.format(task.description),
            'date_expired': task.date_expired,
        }

        # launch test
        self.launch_successfull_test(user, task, params)

    def test_delete_user1_task2(self):
        # Params
        user = self.user1
        task = self.task2
        params = {
            'title': '{}-modified'.format(task.title),
            'description': '{}-modified'.format(task.description),
            'date_expired': task.date_expired,
        }

        # launch test
        self.launch_successfull_test(user, task, params)

    def test_delete_user1_task4(self):
        # Params
        user = self.user1
        task = self.task4
        params = {
            'title': '{}-modified'.format(task.title),
            'description': '{}-modified'.format(task.description),
            'date_expired': task.date_expired,
        }

        # launch test
        self.launch_successfull_test(user, task, params)

    def test_delete_user2_task1(self):
        # Params
        user = self.user2
        task = self.task1

        # send request
        response = self.send_request_with_authenticate(user, task.pk)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)