from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Notification'])
class NotificationView(viewsets.ModelViewSet):
    serializer_class = None  # Placeholder, define your serializer here
    permission_classes = []  # Placeholder, define your permissions here
    def get(self, request):
        return Response("Notification View Response")