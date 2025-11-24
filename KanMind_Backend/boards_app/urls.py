from django.urls import path, include
from boards_app.api import views

urlpatterns = [
    path('email-check/', views.email_check, name='email-check'),
    path('', include('boards_app.api.urls')),
]

