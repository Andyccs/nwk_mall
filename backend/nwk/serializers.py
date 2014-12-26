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
        fields = ('mall_name', 'address', 'region', 'redeem_duration')


class RetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Retail
        fields = ('user',
                  'id',
                  'shop_name',
                  'mall',
                  'category',
                  'logo_url',
                  'location_level',
                  'location_unit',
                  )


class PromotionTypeSerializer(serializers.Serializer):
    promotion_type = serializers.CharField()


class ReadPromotionSerializer(serializers.Serializer):
    def to_native(self, value):
        if isinstance(value, PromotionDiscount):
            a_s = PromotionDiscountSerializer(
                instance=value,
                context=self.context)
            return a_s.data
        if isinstance(value, PromotionReduction):
            b_s = PromotionReductionSerializer(
                instance=value,
                context=self.context)
            return b_s.data
        if isinstance(value, PromotionGeneral):
            c_s = PromotionGeneralSerializer(
                instance=value,
                context=self.context)
            return c_s.data
        raise NotImplementedError


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = ('retail',
                  'title',
                  'description',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  )


class PromotionReductionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PromotionReduction
        fields = ('retail',
                  'title',
                  'description',
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
                  'website',
                  'picture',
                  'point',
                  )


class GrabPromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GrabPromotion
        fields = ('id',
                  'consumer',
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
