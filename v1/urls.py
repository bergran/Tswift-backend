# -*- coding: utf-8 -*-

from rest_framework.routers import SimpleRouter

from v1.views.Boards import BoardView
from v1.views.state import StatesView
from v1.views.tasks import TasksViewset

router = SimpleRouter()
router.register('boards', BoardView)
router.register('states', StatesView)
router.register('tasks', TasksViewset)

urlpatterns = router.urls
