from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'boards', views.BoardViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls)),
]

