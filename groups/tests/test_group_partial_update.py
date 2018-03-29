# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from groups.models.group_profile import GroupProfile


class GroupTestUpdate(APITestCase):
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

    def send_request_without_auth(self, pk, params):
        # get uri
        uri = self.get_uri(pk)

        # send request
        return self.client.patch(uri, params)

    def send_request_with_auth(self, user, pk, params):
        # get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.patch(uri, params)

        # logout
        self.client.logout()

        return response

    def check_serializers_fields(self, payload):
        self.assertIn('id', payload)
        self.assertIn('name', payload)
        self.assertIn('owner', payload)

    def check_payload_has_changes(self, payload, params):
        self.assertEqual(params.get('name'), payload.get('name'))

    def send_request_with_auth(self, user, pk, params):
        # get uri
        uri = self.get_uri(pk)

        # Force login
        self.client.force_login(user)

        # send request
        response = self.client.put(uri, params)

        # logout
        self.client.logout()

        return response

    def launch_successfully_test(self, user, instance, params):
        response = self.send_request_with_auth(user, instance.pk, params)

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check serializers fields are on payload
        self.check_serializers_fields(payload)

        # Check name change
        self.check_payload_has_changes(payload, params)

    def test_update_without_auth(self):
        response = self.send_request_without_auth(self.group1, {
            'name': 'group 1'
        })

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user1(self):
        # params
        user = self.user1
        group = self.group1
        params = {
            'name': '{}-modified'.format(group)
        }
        self.launch_successfully_test(user, group, params)

    def test_update_user1_no_owner(self):
        # params
        user = self.user1
        group = self.group3
        params = {
            'name': '{}-modified'.format(group)
        }
        response = self.send_request_with_auth(user, group.pk, params)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user2(self):
        # params
        user = self.user2
        group = self.group2
        params = {
            'name': '{}-modified'.format(group)
        }
        self.launch_successfully_test(user, group, params)

    def test_update_user3_no_found(self):
        # params
        user = self.user3
        group = self.group1
        params = {
            'name': '{}-modified'.format(group)
        }

        response = self.send_request_with_auth(user, group.pk, params)

        # Check response status is equals to 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
