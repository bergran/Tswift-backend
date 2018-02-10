from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', include_docs_urls(title='Api docs', public=False)),
    path('api/v1/', include('v1.urls')),
    path('api/v1/', include('rest_auth.urls')),
    path('api/v1/registration/', include('rest_auth.registration.urls')),
    path('api/token/verify', verify_jwt_token),
    path('api/token/refresh', refresh_jwt_token)
]
