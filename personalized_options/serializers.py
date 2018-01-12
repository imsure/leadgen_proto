from .models import ActivityPattern
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
    # avail_travel_options = serializers.HiddenField(default='')
    # add_datetime = serializers.HiddenField()
    # mod_datetime = serializers.HiddenField(default=datetime.now())
    # travel_plan_update_datetime = serializers.HiddenField(default=None)

    travel_options = serializers.HyperlinkedIdentityField(view_name='activitypattern-travel-options')

    class Meta:
        model = ActivityPattern
        fields = ('url', 'activity_id', 'metropia_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon',
                  'start_time', 'end_time', 'add_datetime', 'mod_datetime', 'pattern_type',
                  'travel_options', 'owner')
