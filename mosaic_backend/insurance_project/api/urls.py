from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, PolicyViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, PolicyViewSet, MeView # <-- Add MeView

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'policies', PolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'policies', PolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeView.as_view(), name='me'), # <-- Add this line
]