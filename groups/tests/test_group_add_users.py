# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from groups.models.group_profile import GroupProfile


class GroupTestAddUser(APITestCase):
    def setUp(self):
        # add_user some users
        self.user1 = User.objects.create(username='Pepito')
        self.user2 = User.objects.create(username='Benito')
        self.user3 = User.objects.create(username='Menganito')
        self.user4 = User.objects.create(username='Carmelo')

        self.group1 = GroupProfile.objects.create_group(name='Group 1', owner=self.user1)
        self.group1.users.add(self.user1)
        self.group2 = GroupProfile.objects.create_group(name='Group 2', owner=self.user2)
        self.group2.users.add(self.user2)
        self.group3 = GroupProfile.objects.create_group(name='Group 3', owner=self.user3)
        self.group3.users.add(self.user3)
        self.group3.users.add(self.user4)

    def get_uri(self, pk):
        return '/api/v1/groups/{}/add_users/'.format(pk)

    def send_request_without_auth(self, pk, params):
        # get uri
        uri = self.get_uri(pk)

        # send request
        return self.client.post(uri, params)

    def send_request_with_auth(self, user, pk, params):
        # get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.post(uri, params)

        # logout
        self.client.logout()

        return response

    def check_serializers_fields(self, payload):
        self.assertIn('users', payload)

    def launch_successfully_test(self, user, group, params):
        # Send request
        response = self.send_request_with_auth(user, group.pk, params)

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check serializers fields
        self.check_serializers_fields(response.data)

    def test_add_user_without_auth(self):
        response = self.send_request_without_auth(self.group1.pk, {
            'users': [self.user2.pk, self.user3.pk]
        })

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_user_user1(self):
        # params
        user = self.user1
        group = self.group1
        params = {
            'users': [self.user2.pk, self.user3.pk]
        }

        self.launch_successfully_test(user, group, params)

    def test_add_user_user2(self):
        # params
        user = self.user2
        group = self.group2
        params = {
            'users': [self.user1.pk, self.user3.pk]
        }

        self.launch_successfully_test(user, group, params)

    def test_add_user_user3(self):
        # params
        user = self.user3
        group = self.group3
        params = {
            'users': [self.user2.pk, self.user1.pk]
        }

        self.launch_successfully_test(user, group, params)

    def test_add_user_duplicated(self):
        # params
        user = self.user3
        group = self.group3
        params = {
            'users': [self.user1.pk, self.user2.pk, self.user3.pk]
        }

        response = self.send_request_with_auth(user, group.pk, params)

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Chec
        self.assertIn('users', response.data)

    def test_add_user_no_owner(self):
        # params
        user = self.user4
        group = self.group3
        params = {
            'users': [self.user1.pk, self.user2.pk, self.user3.pk]
        }

        response = self.send_request_with_auth(user, group.pk, params)

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

