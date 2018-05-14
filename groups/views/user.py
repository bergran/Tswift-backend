# -*- coding: utf-8 -*-
from django.conf import settings
from rest_auth.app_settings import create_token
from rest_auth.utils import jwt_encode
from rest_auth.registration.views import RegisterView


class UserViewSet(RegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)
        return user
