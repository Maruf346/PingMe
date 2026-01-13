from django.urls import path
from . import views

urlpatterns = [
    path('dummy/', views.NotificationView.as_view({'get': 'list'}), name='notification-dummy'),
]
