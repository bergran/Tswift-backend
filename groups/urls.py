# -*- coding: utf-8 -*-

from rest_framework.routers import SimpleRouter

from groups.views.group import GroupsViewSet

router = SimpleRouter()
router.register('groups', GroupsViewSet)

urlpatterns = router.urls
