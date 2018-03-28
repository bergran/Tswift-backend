# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from groups.models.group_profile import GroupProfile


class GroupTestCreate(APITestCase):
    def setUp(self):
        # Create some users
        self.user1 = User.objects.create(username='Pepito')
        self.user2 = User.objects.create(username='Benito')
        self.user3 = User.objects.create(username='Menganito')

    def get_uri(self):
        return '/api/v1/groups/'

    def send_request_without_auth(self, params):
        # get uri
        uri = self.get_uri()

        # send request
        return self.client.post(uri, params)

    def send_request_with_auth(self, user, params):
        # get uri
        uri = self.get_uri()

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.post(uri, params)

        # logout
        self.client.logout()

        return response

    def check_serializers_fields(self, payload):
        self.assertIn('id', payload)
        self.assertIn('name', payload)
        self.assertIn('owner', payload)

    def launch_successfully_test(self, user, params):
        # Send request
        response = self.send_request_with_auth(user, params)

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check serializers fields
        self.check_serializers_fields(response.data)

    def test_create_without_auth(self):
        response = self.send_request_without_auth({
            'name': 'Group 1'
        })

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user1(self):
        # params
        user = self.user1
        params = {
            'name': 'Group 1'
        }

        self.launch_successfully_test(user, params)

    def test_create_user2(self):
        # params
        user = self.user2
        params = {
            'name': 'Group 2'
        }

        self.launch_successfully_test(user, params)

    def test_create_user3(self):
        # params
        user = self.user3
        params = {
            'name': 'Group 3'
        }

        self.launch_successfully_test(user, params)

    def test_create_user1_duplicate(self):
        # params
        user = self.user1
        params = {
            'name': 'Group 4'
        }

        self.launch_successfully_test(user, params)

        response = self.send_request_with_auth(user, params)

        # Check response status code is equals to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

