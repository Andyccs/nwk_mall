from django.contrib.auth.models import User, Group
from nwk.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Retail
        fields = ('user',
                  'shop_name',
                  'logo_url',
                  'location_level',
                  'location_unit',
                  )


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = ('retail',
                  'title',
                  'description',
                  'quantity',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  )


class PromotionPriceReductionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionPriceReduction
        fields = ('retail',
                  'title',
                  'description',
                  'quantity',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  'original_price',
                  'discount_price',
                  )


class PromotionDiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionDiscount
        fields = ('retail',
                  'title',
                  'description',
                  'quantity',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  'discount',
                  )


class PromotionGeneralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionGeneral
        fields = ('retail',
                  'title',
                  'description',
                  'quantity',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  'price',
                  )


class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumer
        fields = ('user',
                  'favorite_shops',
                  'grabbed',
                  'website',
                  'picture',
                  'point',
                  )

class GrabPromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Consumer
        fields = ('user',
                  'favorite_shops',
                  'grabbed',
                  'website',
                  'picture',
                  'point',
                  )


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ('customer',
                  'badge',
                  'device_token',
                  'device_type',
                  'timezone',
                  'app_name',
                  'app_version',
                  )
