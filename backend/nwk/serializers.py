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


class MallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mall
        fields = ('mall_name', 'address', 'region')


class RetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Retail
        fields = ('user',
                  'shop_name',
                  'mall',
                  'logo_url',
                  'location_level',
                  'location_unit',
                  )


class PromotionTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionType
        fields = ('promotion_type')


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = ('retail',
                  'title',
                  'promotion_type',
                  'description',
                  'quantity',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  'price',
                  )


class PromotionPriceReductionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionPriceReduction
        fields = (
                  # 'retail',
                  # 'title',
                  # 'description',
                  # 'quantity',
                  # 'time_expiry',
                  # 'image_url',
                  # 'created_at',
                  'original_price',
                  'discount_price',
                  )


class PromotionPriceDiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionPriceDiscount
        fields = (
                  # 'retail',
                  # 'title',
                  # 'description',
                  # 'quantity',
                  # 'time_expiry',
                  # 'image_url',
                  # 'created_at',
                  'discount',
                  )


class PromotionPriceGeneralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionPriceGeneral
        fields = (
                  # 'retail',
                  # 'title',
                  # 'description',
                  # 'quantity',
                  # 'time_expiry',
                  # 'image_url',
                  # 'created_at',
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
        model = GrabPromotion
        fields = ('consumer',
                  'promotion',
                  'redeem_time',
                  'is_approved',
                  'qr_code_url',
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
