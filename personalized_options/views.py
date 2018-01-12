from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework import renderers
from .serializers import ActivityPatternSerializer, UserSerializer
from .models import ActivityPattern
from .permissions import IsOwnerOrReadOnly
from datetime import datetime


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ActivityPatternViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `delete` actions against activity patterns.
    """
    queryset = ActivityPattern.objects.all()
    serializer_class = ActivityPatternSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(mod_datetime=datetime.now(), owner=self.request.user)

    @detail_route(methods=['get'])
    def travel_options(self, request, *args, **kwargs):
        activity_pattern = self.get_object()
        data = {'Available Travel Options': activity_pattern.avail_travel_options,
                'Last Update Time': activity_pattern.travel_plan_update_datetime}
        return Response(data=data)


@api_view(['GET'])
def travel_plan(request, pk, format=None):
    if request.method == 'GET':
        return Response("travel plans")
