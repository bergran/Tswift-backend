# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class BoardTestCreate(APITestCase):
    def setUp(self):
        # Create some users
        self.user = User.objects.create(username='Pepito')

    def send_request_with_authenticate(self, user, params):
        self.client.force_login(user=user)
        response = self.client.post('/api/v1/boards/', params)
        self.client.logout()
        return response

    def send_request_without_authenticate(self, params):
        return self.client.post('/api/v1/boards/', params)

    def test_create_without_auth(self):
        # Params
        board_name = 'no auth'
        
        # Send request
        response = self.send_request_without_authenticate({
            'name': board_name
        })
        
        # Check response status code == 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_with_auth(self):
        # Params
        board_name = 'Pepito board'
        
        # Send request
        response = self.send_request_with_authenticate(
            self.user,
            {
                'name': board_name
            }
        )
        
        # Check response status code == 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        payload = response.data
        # Check serializers fields are on payload
        self.assertIn('id', payload.keys())
        self.assertIn('name', payload.keys())
        self.assertIn('date_created', payload.keys())
        self.assertIn('date_modified', payload.keys())

        # Check payload name is equals to board_name
        self.assertEqual(payload.get('name', None), board_name)