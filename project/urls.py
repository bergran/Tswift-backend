from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('v1.urls')),
    path('api/token/verify', verify_jwt_token),
    path('api/token/refresh', refresh_jwt_token)
]
