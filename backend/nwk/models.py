from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


POINT_DEFAULT = 100
GROUP_RETAIL = "retail"
GROUP_CONSUMER = "consumer"


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


# class PromotionType(models.Model):
#     GENERAL = 'GEN'
#     DISCOUNT = 'DIS'
#     REDUCTION = 'RED'
#     PROMOTION_TYPES = (
#         (GENERAL, 'GENERAL'),
#         (DISCOUNT, 'DISCOUNT'),
#         (REDUCTION, 'REDUCTION')
#         )

#     promotion_type = models.CharField(
#         max_length=3,
#         choices=PROMOTION_TYPES,
#         default=GENERAL,
#         primary_key=True)

#     def __str__(self):
#         return "%s" % self.promotion_type


class Promotion(models.Model):
    retail = models.ForeignKey(Retail)

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    time_expiry = models.DateTimeField(auto_now=True)  # must be > current time
    image_url = models.CharField(max_length=300)
    created_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On creation, update timestamps '''
        if self.pk is None:
            self.created_at = timezone.make_aware(
                datetime.datetime.now(),
                timezone.get_default_timezone())
        return super(Promotion, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % self.title


class PromotionReduction(Promotion):
    # support up to million dollar
    original_price = models.DecimalField(max_digits=9,
                                         decimal_places=2)
    # support up to million dollar
    discount_price = models.DecimalField(max_digits=9,
                                         decimal_places=2)

    def __str__(self):
        return "from %d to %d" % (self.original_price, self.discount_price)


class PromotionDiscount(Promotion):
    discount = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%d discount" % self.discount


class PromotionGeneral(Promotion):
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
    picture = models.FileField(upload_to='USER/CONSUMER/PICTURE/', blank=True)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s" % self.user

BOOLEAN_CHOICES = (
    (None, 'Waiting'),
    (True, 'Yes'),
    (False, 'No')
)


class GrabPromotion(models.Model):
    # class Meta:
    #     # does not allow multiple promotion grabbing
    #     unique_together = ['consumer', 'promotion']

    consumer = models.ForeignKey(Consumer)
    promotion = models.ForeignKey(Promotion)

    # deadline for the consumer to redeem the promotion
    # past this, the entry will be invalid
    redeem_time = models.DateTimeField(editable=False)

    is_approved = models.NullBooleanField(
        blank=True,
        null=True,
        choices=BOOLEAN_CHOICES)

    __original_is_approved = None

    qr_code_url = models.URLField(blank=True)

    point = models.PositiveIntegerField(
        blank=True, default=POINT_DEFAULT, editable=False)

    def __init__(self, *args, **kwargs):
        super(GrabPromotion, self).__init__(*args, **kwargs)
        self.__original_is_approved = self.is_approved

    def save(self, *args, **kwargs):
        '''
        On creation:
        - set redeem time
        - set point
        - get QR code url
        '''
        if self.pk is None:
            mall = self.promotion.retail.mall
            redeem_duration = mall.redeem_duration

            # set time
            now = datetime.datetime.now()
            duration = datetime.timedelta(minutes=redeem_duration)
            self.redeem_time = timezone.make_aware(
                now + duration,
                timezone.get_default_timezone())

            # set point
            self.point = POINT_DEFAULT

        # auto add consumer point on successful redeem
        if self.__original_is_approved is None and self.is_approved:
            consumer = self.consumer
            consumer.point = consumer.point + self.point
            consumer.save()

        super(GrabPromotion, self).save(*args, **kwargs)
        self.__original_is_approved = self.is_approved

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
