"""
URL configuration for KanMind project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'KanMind API',
        'endpoints': {
            'auth': '/api/registration/, /api/login/',
            'boards': '/api/boards/',
            'tasks': '/api/tasks/',
            'email-check': '/api/email-check/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth_app.urls')),
    path('api/', include('boards_app.urls')),
    path('api/', include('tasks_app.urls')),
    path('api/', api_root, name='api-root'),
]

