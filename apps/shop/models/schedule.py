from datetime import datetime, timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from apps.common.behaviors import Timestampable

# from datetime import datetime, timedelta
# any_day = datetime(2004, 3, 27)
# monday = any_day - timedelta(days=any_day.weekday())
# WEEKDAYS = [
#     (day_num, (monday+timedelta(days=day_num)).strftime("%A")) for day_num in range(7)
# ]
WEEKDAY_CHOICES = [
    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
]


class Schedule(Timestampable, models.Model):
    """
    A schedule for when a menu is available.
    Can be used by menu items to restrict availability (eg. breakfast vs dinners items)
    """

    menu = models.ForeignKey('shop.Menu', on_delete=models.CASCADE, related_name="schedules")
    name = models.CharField(max_length=30, default="open hours")

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    available_weekdays = ArrayField(
        models.IntegerField(choices=WEEKDAY_CHOICES),
        default=list, blank=True, help_text='list of weekdays when schedule applies'
    )

    # MODEL PROPERTIES
    @property
    def shop(self):
        return self.menu.shop

    @property
    def is_on_now(self) -> bool:
        if not all([
            self.menu.shop.timezone,
            self.start_time, self.end_time,
            len(self.available_weekdays)
        ]):
            return False
        shop_datetime = datetime.now() + self.shop.timezone.utcoffset(datetime.now())
        if shop_datetime.weekday() in self.available_weekdays:
            if self.start_time <= shop_datetime.time() <= self.end_time:
                return True
        return False

    @property
    def time_until_next_on(self) -> timedelta:
        # todo: write this method
        return timedelta(minutes=5)

    # MODEL FUNCTIONS
