from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


class ActivityPatternViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `delete` actions against activity patterns.
    """
    queryset = ActivityPattern.objects.all()
    serializer_class = ActivityPatternSerializer
