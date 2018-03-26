# -*- coding: utf-8 -*-

from rest_framework.routers import SimpleRouter

from v1.views.Boards import BoardView
from v1.views.state import StatesView
from v1.views.tasks import TasksViewset
from v1.views.Permissions import PermissionView

router = SimpleRouter()
router.register('boards', BoardView)
router.register('states', StatesView)
router.register('tasks', TasksViewset)
router.register('permissions', PermissionView, base_name='Permissions')

urlpatterns = router.urls
