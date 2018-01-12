from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework import renderers
from .serializers import ActivityPatternSerializer, UserSerializer
from .models import ActivityPattern, Driving, Walking, Biking
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
        if not activity_pattern.avail_travel_options:
            options_dict = {}
        else:
            options = activity_pattern.avail_travel_options.split(',')
            base_url = request.build_absolute_uri()
            urls = [base_url + opt for opt in options]
            options_dict = {}
            for opt, url in zip(options, urls):
                options_dict[opt] = url

        data = {
            '# of available travel options': len(options_dict),
            'Available Travel Options': options_dict,
            'Last Update Time': activity_pattern.travel_plan_update_datetime
        }
        return Response(data=data)


@api_view(['GET'])
def travel_option(request, pk, mode, format=None):
    activity_pattern = ActivityPattern.objects.get(pk=pk)
    options = activity_pattern.avail_travel_options.split(',')
    if request.method == 'GET':
        if mode in options:
            ModeClass = eval(mode.title())
            option = ModeClass.objects.get(activity_id_id=pk)
            fields = [f.name for f in ModeClass._meta.fields]
            data = {}
            for field in fields:
                if field == 'activity_id' or field == 'id':
                    continue
                data[field] = getattr(option, field)

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'Error': 'mode {} is not available for this activity pattern.'.format(mode)},
                            status=status.HTTP_400_BAD_REQUEST)
