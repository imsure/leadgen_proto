from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    activity_patterns = serializers.HyperlinkedRelatedField(many=True,
                                                            view_name='activity-patterns',
                                                            read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'activity_patterns')


class ActivityPatternSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = ActivityPattern
        fields = ('url', 'activity_id', 'metropia_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon',
                  'start_time', 'end_time', 'add_datetime', 'mod_datetime',
                  'travel_plan_update_datetime', 'avail_travel_options', 'owner')
