# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from groups.models.group_profile import GroupProfile


class GroupTestList(APITestCase):
    def setUp(self):
        # Create some users
        self.user1 = User.objects.create(username='Pepito')
        self.user2 = User.objects.create(username='Benito')
        self.user3 = User.objects.create(username='Menganito')

        # Create some groups
        self.group1 = GroupProfile.objects.create_group(name='group 1', owner=self.user1)
        self.group1.user_set.add(self.user1)

        self.group2 = GroupProfile.objects.create_group(name='group 2', owner=self.user2)
        self.group2.user_set.add(self.user1)
        self.group2.user_set.add(self.user2)

        self.group3 = GroupProfile.objects.create_group(name='group 3', owner=self.user3)
        self.group3.user_set.add(self.user1)
        self.group3.user_set.add(self.user3)

    def get_uri(self):
        return '/api/v1/groups/'

    def send_request_without_auth(self):
        # get uri
        uri = self.get_uri()

        # send request
        return self.client.get(uri)

    def send_request_with_auth(self, user, params={}):
        # get uri
        uri = self.get_uri()

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.get(uri, params)

        # logout
        self.client.logout()

        return response

    def check_serializers_fields(self, payload):
        self.assertIn('id', payload.get('results')[0])
        self.assertIn('name', payload.get('results')[0])
        self.assertIn('owner', payload.get('results')[0])

    def test_list_without_auth(self):
        response = self.send_request_without_auth()

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user1(self):
        # params
        user = self.user1

        response = self.send_request_with_auth(user)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

        # Check has same len results
        self.assertEqual(payload.get('count'), 3)

    def test_list_user1_with_params(self):
        # params
        user = self.user1

        response = self.send_request_with_auth(user, {
            'owner': self.group1.owner.username
        })

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

        # Check has same len results
        self.assertEqual(payload.get('count'), 1)

    def test_list_user2(self):
        # params
        user = self.user2

        response = self.send_request_with_auth(user)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

        # Check has same len results
        self.assertEqual(payload.get('count'), 1)

    def test_list_user3(self):
        # params
        user = self.user3

        response = self.send_request_with_auth(user)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

        # Check has same len results
        self.assertEqual(payload.get('count'), 1)
