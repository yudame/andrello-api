from datetime import timedelta

import pytz
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES
from simple_history.models import HistoricalRecords

from apps.common.behaviors import Timestampable, Locatable, Contactable, Translatable, Permalinkable
from settings import AUTH_USER_MODEL


class Shop(Timestampable, Locatable, Contactable, Translatable, Permalinkable, models.Model):

    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="shop")
    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    logo_image = models.OneToOneField('common.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='shop_as_logo',
                                      help_text='if not square will be padded, like a social media profile pic')
    icon_image = models.OneToOneField('common.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='shop_as_icon',
                                      help_text='version of the logo that fits in a small square')

    pushover_user_key = models.CharField(max_length=30, default="", blank=True)
    pushover_device_name = models.CharField(max_length=25, default="", blank=True)

    # SOCIAL ACCOUNTS
    facebook_href = models.URLField(default="", blank=True)
    instagram_href = models.URLField(default="", blank=True)
    google_maps_href = models.URLField(default="", blank=True)
    trip_advisor_href = models.URLField(default="", blank=True)

    # SETTINGS
    is_ghost_location = models.BooleanField(default=False)
    currency = CurrencyField(default='THB')

    # INTERFACES: BOTS AND WEBSITES
    # line_channel = line_app.LineChannel
    # website = website.Website

    gramables = models.ManyToManyField('common.Image', blank=True)

    # INHERITED FIELDS:
    # address, latitude, longitude
    # contact_name, contact_phone, contact_email
    # base_language, language


    # HISTORY MANAGER
    # history = HistoricalRecords()

    # MODEL PROPERTIES

    @property
    def customer_line_channel(self):
        from apps.line_app.models.line_channel import LineChannel, CUSTOMER_CHANNEL
        return LineChannel.objects.filter(shop=self, channel_type=CUSTOMER_CHANNEL).first()

    @property
    def orders(self):
        from apps.shop.models import Order
        return Order.objects.filter(line_channel_membership__line_channel__shop_id=self.id)

    @property
    def is_open(self) -> bool:
        return any([
            schedule.is_on_now for schedule in self.menu.schedules.all()
        ])

    @property
    def time_until_next_open(self) -> timedelta:
        return min([
            schedule.time_until_next_on for schedule in self.menu.schedules.all()
        ])

    # MODEL FUNCTIONS
    def setup_related_models(self):
        from apps.line_app.models.line_channel import LineChannel, CUSTOMER_CHANNEL
        line_channel, lc_created = LineChannel.objects.get_or_create(shop=self, channel_type=CUSTOMER_CHANNEL)
        from apps.shop.models import Menu, Schedule
        menu, m_created = Menu.objects.get_or_create(shop=self)
        if not Schedule.objects.filter(menu=menu).exists():
            schedule = Schedule.objects.create(menu=menu, available_weekdays=list(range(7)))
            if not self.timezone:
                self.timezone = pytz.timezone('Asia/Bangkok')
                self.save()

    def __str__(self):
        return self.name or f"Shop {self.id}"

    def reset_slug(self):
        self.slug = slugify(self.name)

    # @models.permalink
    # def get_absolute_url(self):
    #     url_kwargs = self.get_url_kwargs(slug=self.slug)
    #     return (self.url_name, (), url_kwargs)

    def get_absolute_url(self):
        return reverse('shop:shop', kwargs={'shop_slug': self.slug})

    # META
    class Meta:
        ordering = ('name',)
        unique_together = ('owner', 'name')


@receiver(pre_save, sender=Shop)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.reset_slug()

@receiver(post_save, sender=Shop)
def post_save_related_models(sender, instance, created, *args, **kwargs):
    if created:
        instance.setup_related_models()

