from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]