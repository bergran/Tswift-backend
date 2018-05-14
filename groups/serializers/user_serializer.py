# -*- coding: utf-8 -*-
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(RegisterSerializer):
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user
