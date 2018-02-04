# -*- coding: utf-8 -*-

from rest_framework.routers import SimpleRouter

from v1.views.Boards import BoardView

router = SimpleRouter()
router.register('boards', BoardView)

urlpatterns = router.urls
