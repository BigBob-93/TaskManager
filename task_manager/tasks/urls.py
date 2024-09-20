from django.urls import path

from .views import TaskViewSet

urlpatterns = [
    path(r'<str:pk>/', TaskViewSet.as_view(
        {
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy',
        }
    ), name='task'),
    path('', TaskViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    ), name='tasks')
]
