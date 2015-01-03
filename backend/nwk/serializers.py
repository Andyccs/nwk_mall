from django.contrib.auth.models import User, Group
from nwk.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email', 'groups',)


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
        raise NotImplementedError("Promotion Type Unknown. Value: "+str(value))


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = ('retail',
                  'title',
                  'description',
                  'time_expiry',
                  'image_url',
                  'created_at',
                  'id',
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
                  'id',
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
                  'id',
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
                  'id',
                  )


class ConsumerSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Consumer
        fields = ('id',
                  'username',
                  'password',
                  'email',
                  'favorite_shops',
                  'picture',
                  'point',
                  )

    def restore_object(self, attrs, instance=None):
        if instance:  # Update
            instance.picture = attrs['picture']
            user = instance.user
            user.username = attrs['user.username']
            user.email = attrs['user.email']
            instance.user = user
        else:
            user = User.objects.create_user(
                username=attrs['user.username'], email=attrs['user.email'])
            user.group = Group(name="consumer")
            user.save()
            instance = Consumer(
                user=user, picture=attrs['picture'])
        user.set_password(attrs['user.password'])
        return instance


class ReadGrabPromotionSerializer(serializers.HyperlinkedModelSerializer):
    consumer = ConsumerSerializer()
    promotion = PromotionSerializer()

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
