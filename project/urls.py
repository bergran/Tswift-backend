from allauth.account.views import ConfirmEmailView
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token

from groups.views.user import UserViewSet

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/docs/', include_docs_urls(title='Api docs', public=False)),
    path('api/v1/', include('v1.urls')),
    path('api/v1/', include('groups.urls')),
    path('api/v1/', include('rest_auth.urls')),
    path('api/v1/register/', UserViewSet.as_view()),
    path('api/token/verify', verify_jwt_token),
    path('api/token/refresh', refresh_jwt_token)
]
