from .models import ActivityPattern, Driving, WalkTransit
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    activity_patterns = serializers.HyperlinkedRelatedField(
        many=True,
        # <modelname>-detail for standard router class
        view_name='activitypattern-detail',
        read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'activity_patterns')


class ActivityPatternSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    travel_options = serializers.HyperlinkedIdentityField(view_name='activitypattern-travel-options')

    class Meta:
        model = ActivityPattern
        fields = ('url', 'activity_id', 'metropia_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon',
                  'start_time', 'end_time', 'add_datetime', 'mod_datetime', 'pattern_type',
                  'travel_options', 'owner')


class DrivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driving
        fields = ('activity_id', 'cost', 'wait_time', 'travel_time', 'congestion_level')


class WalkTransitSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkTransit
        fields = ('activity_id', 'cost', 'wait_time', 'travel_time')
