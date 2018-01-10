from django.db import models


class ActivityPattern(models.Model):
    """
    Activity patterns inferred from Metropia users trip data.
    """
    # fields
    activity_id = models.PositiveIntegerField(primary_key=True, db_index=True)
    metropia_id = models.IntegerField(help_text='Unique ID for each Metropia user')
    from_lat = models.FloatField(help_text='Start latitude')
    from_lon = models.FloatField(help_text='Start longitude')
    to_lat = models.FloatField(help_text='End latitude')
    to_lon = models.FloatField(help_text='End longitude')
    start_time = models.TimeField(help_text='Start time of the activity')
    end_time = models.TimeField(help_text='End time of the activity')
    add_datetime = models.DateTimeField(auto_now_add=True,
                                        help_text='Date & time when this activity pattern was added')
    mod_datetime = models.DateTimeField(auto_now_add=True,
                                        help_text='Date & time when this activity pattern was last modified')
    travel_plan_update_datetime = models.DateTimeField(
        blank=True, null=True,
        help_text='Date & time when travel plans for this activity pattern was updated')
    avail_travel_options = models.TextField(
        blank=True,
        help_text='A list of available travel options for this activity pattern')

    class Meta:
        # ordering = ('metropia_id',)
        db_table = 'activity_pattern'  # override default table name derived by Django
        # the default field(s) to use in model Manager’s latest() and earliest() methods.
        get_latest_by = ('travel_plan_update_datetime', 'mod_datetime', 'add_datetime')
        indexes = [
            models.Index(fields=['activity_id'], name='activity_id_idx'),
            # Good for queries like:
            # SELECT count(activity_id) from activity_pattern where metropia_id = xxx;
            # or
            # SELECT * from activity_pattern metropia_id = xxx and activity_id = yyy;
            # Be aware that more indexes -> slower updates
            # models.Index(fields=['metropia_id', 'activity_id']),
        ]


class TravelOption(models.Model):
    """
    An abstract base class for multi-modal travel plans
    """
    # common fields among all plans
    cost = models.FloatField()
    # 0 for driving, walking and biking modes
    wait_time = models.IntegerField()  # in seconds
    travel_time = models.IntegerField()  # in seconds
    # Be aware that by default Django will create BTree index on foreignkey field
    activity_id = models.ForeignKey(ActivityPattern, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Driving(TravelOption):
    congestion_level = models.IntegerField()

    class Meta(TravelOption.Meta):
        db_table = 'driving'


class WalkTransit(TravelOption):
    """
    Walking + Public transit
    """

    class Meta(TravelOption.Meta):
        db_table = 'walk_transit'


class BikeTransit(TravelOption):
    """
    Biking + Public transit
    """

    class Meta(TravelOption.Meta):
        db_table = 'bike_transit'


class ParkAndRide(TravelOption):
    """
    Park and Ride
    """

    class Meta(TravelOption.Meta):
        db_table = 'park_and_ride'


class KissAndRide(TravelOption):
    """
    Kiss and Ride
    """

    class Meta(TravelOption.Meta):
        db_table = 'kiss_and_ride'


class BikeAndRide(TravelOption):
    """
    Bike and Ride
    """

    class Meta(TravelOption.Meta):
        db_table = 'bike_and_ride'


class Walking(TravelOption):
    """
    Walk only, cost and wait time are zero
    """

    class Meta(TravelOption.Meta):
        db_table = 'walking'


class Biking(TravelOption):
    """
    Bike only, cost and wait time are zero
    """

    class Meta(TravelOption.Meta):
        db_table = 'biking'


class Uber(TravelOption):
    """
    UberX: private ride at an everyday price
    UberXL: Affordable SUVs for groups up to 6
    UberPool: Shared rides, shared cost
    """
    cost_low = models.IntegerField()  # low estimate
    high_low = models.IntegerField()  # high estimate
    product = models.CharField(max_length=100)  # product name

    class Meta(TravelOption.Meta):
        db_table = 'uber'
