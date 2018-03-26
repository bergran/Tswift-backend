# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class PermissionsTestList(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Pepito')

    def test_list_permissions_without_auth(self):
        # Send request
        response = self.client.get('/api/v1/permissions/')

        # Check response status code is equals to 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_permissions_with_auth(self):
        # Force login
        self.client.force_login(self.user)

        # Send request
        response = self.client.get('/api/v1/permissions/')

        # Check response status code is equals to 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.data
        # Check permissions are on payload
        self.assertIn('read', payload)
        self.assertIn('write', payload)
        self.assertIn('delete', payload)
