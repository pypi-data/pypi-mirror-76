from rest_framework import routers
from fagsoft.permissions.views import (
    PermissionViewSet,
    GroupViewSet
)

router = routers.DefaultRouter()
router.register(r'permissions', PermissionViewSet)
router.register(r'permissions_groups', GroupViewSet)
