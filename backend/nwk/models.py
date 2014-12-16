from django.db import models
import datetime
from django.contrib.auth.models import User


class Mall(models.Model):
    mall_name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    region = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % self.mall_name


class Retail(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    mall = models.ForeignKey(Mall)

    shop_name = models.CharField(max_length=30)
    logo_url = models.URLField(blank=True)
    location_level = models.PositiveSmallIntegerField()
    location_unit = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s" % self.shop_name


class PromotionType(models.Model):
    GENERAL = 'GEN'
    DISCOUNT = 'DIS'
    REDUCTION = 'RED'
    PROMOTION_TYPES = (
        (GENERAL, 'GENERAL'),
        (DISCOUNT, 'DISCOUNT'),
        (REDUCTION, 'REDUCTION')
        )

    promotion_type = models.CharField(
        max_length=3,
        choices=PROMOTION_TYPES,
        default=GENERAL,
        primary_key=True)

    def __str__(self):
        return "%s" % self.promotion_type


class PromotionPrice(models.Model):
    pass


class Promotion(models.Model):
    retail = models.ForeignKey(Retail)
    promotion_type = models.ForeignKey(PromotionType)

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    quantity = models.PositiveSmallIntegerField()  # up to 32767
    time_expiry = models.DateTimeField(auto_now=True)  # must be > current time
    image_url = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    # TODO: add price
    price = models.OneToOneField(PromotionPrice)

    def __str__(self):
        return "%s" % self.title


class PromotionPriceReduction(PromotionPrice):
    # support up to million dollar
    original_price = models.DecimalField(max_digits=9,
                                         decimal_places=2)
    # support up to million dollar
    discount_price = models.DecimalField(max_digits=9,
                                         decimal_places=2)

    def __str__(self):
        return "from %d to %d" % (self.original_price, self.discount_price)


class PromotionPriceDiscount(PromotionPrice):
    discount = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%d discount" % self.discount


class PromotionPriceGeneral(PromotionPrice):
    # support up to million dollar
    price = models.DecimalField(max_digits=9,
                                decimal_places=2)

    def __str__(self):
        return "%d" % self.price


class Consumer(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    favorite_shops = models.ManyToManyField(Retail, blank=True)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.URLField(blank=True)
    point = models.PositiveIntegerField()

    def __str__(self):
        return "%s" % self.user


class GrabPromotion(models.Model):
    consumer = models.ForeignKey(Consumer)
    promotion = models.ForeignKey(Promotion)

    # deadline for the consumer to redeem the promotion
    # past this, the entry will be invalid
    # the customer must grab again
    redeem_time = models.DateTimeField(auto_now=True)  # must be > current time

    is_approved = models.BooleanField(default=False)
    qr_code_url = models.URLField()
    point = models.PositiveIntegerField()

    def __str__(self):
        return "%s by %s" % (self.promotion, self.customer)


class Application(models.Model):
    customer = models.ForeignKey(Consumer)

    badge = models.PositiveIntegerField()
    device_token = models.CharField(max_length=250)
    device_type = models.CharField(max_length=6)
    timezone = models.CharField(max_length=20, default='Asia/Singapore')
    app_name = models.CharField(max_length=20)
    app_version = models.PositiveIntegerField()

    def __str__(self):
        return "%s" % self.customer
