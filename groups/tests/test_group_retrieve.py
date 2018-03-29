# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from groups.models.group_profile import GroupProfile


class GroupTestRetrieve(APITestCase):
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

    def get_uri(self, pk):
        return '/api/v1/groups/{}/'.format(pk)

    def send_request_without_auth(self, pk):
        # get uri
        uri = self.get_uri(pk)

        # send request
        return self.client.get(uri)

    def send_request_with_auth(self, user, pk, params={}):
        # get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.get(uri, params)

        # logout
        self.client.logout()

        return response

    def check_serializers_fields(self, payload):
        self.assertIn('id', payload)
        self.assertIn('name', payload)
        self.assertIn('owner', payload)

    def test_retrieve_without_auth(self):
        response = self.send_request_without_auth(self.group1.pk)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_group1(self):
        # params
        user = self.user1
        group = self.group1

        response = self.send_request_with_auth(user, group.pk)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

    def test_retrieve_group2(self):
        # params
        user = self.user1
        group = self.group2

        response = self.send_request_with_auth(user, group.pk)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)

    def test_retrieve_group3(self):
        # params
        user = self.user1
        group = self.group3

        response = self.send_request_with_auth(user, group.pk)

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializer fields are on payload
        self.check_serializers_fields(payload)
