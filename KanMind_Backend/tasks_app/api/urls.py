from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

# Nested router for comments
tasks_router = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', views.CommentViewSet, basename='task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
]

