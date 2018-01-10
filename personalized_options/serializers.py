from .models import *
from rest_framework import serializers


class ActivityPatternSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityPattern
        fields = ('url', 'activity_id', 'metropia_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon',
                  'start_time', 'end_time', 'add_datetime', 'mod_datetime',
                  'travel_plan_update_datetime', 'avail_travel_options')
