from django.contrib.auth.models import User
from django.db import models


class Mall(models.Model):
    mall_name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    region = models.CharField(max_length=30)
    redeem_duration = models.PositiveIntegerField()  # in minutes

    def __str__(self):
        return "%s" % self.mall_name


class Retail(models.Model):
    CAT_FOOD = 'FOOD'
    CAT_FASHION = 'FASHION'
    CAT_LIFESTYLE = 'LIFESTYLE'
    CAT_OTHER = 'OTHER'
    PROMOTION_CATEGORIES = (
        (CAT_FOOD, 'FOOD'),
        (CAT_FASHION, 'FASHION'),
        (CAT_LIFESTYLE, 'LIFESTYLE'),
        (CAT_OTHER, 'OTHER'),
        )

    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    mall = models.ForeignKey(Mall)

    shop_name = models.CharField(max_length=30)
    logo_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=PROMOTION_CATEGORIES,
        default=CAT_OTHER)
    location_level = models.PositiveSmallIntegerField()
    location_unit = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s" % self.shop_name
