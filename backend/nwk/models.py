from django.db import models
import datetime
from django.contrib.auth.models import User


class Retail(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    shop_name = models.CharField(max_length=30)
    logo_url = models.URLField(blank=True)
    location_level = models.PositiveSmallIntegerField()
    location_unit = models.PositiveSmallIntegerField()


# Create your models here.
class Promotion(models.Model):
    retail = models.ForeignKey(Retail)

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    quantity = models.PositiveSmallIntegerField()  # up to 32767
    time_expiry = models.DateTimeField(auto_now=True)  # must be > current time
    image_url = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.datetime.now())


class PromotionPriceReduction(Promotion):
    original_price = models.DecimalField(max_digits=9, decimal_places=2)  # support up to million dollar
    discount_price = models.DecimalField(max_digits=9, decimal_places=2)  # support up to million dollar


class PromotionDiscount(Promotion):
    discount = models.PositiveSmallIntegerField()


class PromotionGeneral(Promotion):
    price = models.DecimalField(max_digits=9, decimal_places=2)  # support up to million dollar


class Consumer(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    favorite_shops = models.ManyToManyField(Retail)
    grabbed = models.ManyToManyField(Promotion)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.URLField(blank=True)
    point = models.PositiveIntegerField()


class Installation(models.Model):
    customer = models.ForeignKey(Consumer)

    badge = models.PositiveIntegerField()
    device_token = models.CharField(max_length=250)
    device_type = models.CharField(max_length=6)
    timezone = models.CharField(max_length=20, default='Asia/Singapore')
    app_name = models.CharField(max_length=20)
    app_version = models.PositiveIntegerField()
