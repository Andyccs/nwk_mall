from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import (IsAuthenticated, IsAdminUser,
                                        DjangoObjectPermissions, AllowAny)

from nwk.permissions import *
from nwk.serializers import *
import itertools


@api_view(['POST'])
def register(request):
    """
    API endpoint that allows registration of consumers.
    """
    VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
    DEFAULTS = {
        # you can define any defaults that you would like for the user, here
    }
    user_data = {field: data for (field, data) in request.DATA.items() if field in VALID_USER_FIELDS}
    user_data.update(DEFAULTS)
    try:
        user = get_user_model().objects.create_user(
            **user_data)
        consumer = Consumer(user=user)
        if 'picture' in request.FILES:
            consumer.picture = request.FILES['picture']
        consumer.save()
        serializer = ConsumerSerializer(
            instance=consumer,
            context={'request': request}
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    # def get_permissions(self):
    #     # allow non-authenticated user to create via POST
    #     return (AllowAny() if self.request.method == 'POST'
    #             else IsStaffOrTargetUser()),

    def list(self, request):
        username = self.request.QUERY_PARAMS.get('username', None)
        if username is not None:
            try:
                user = User.objects.get(username=username)
                if user.groups.all()[0].name == GROUP_CONSUMER:
                    queryset = Consumer.objects.get(user=user)
                    serializer = ConsumerSerializer(
                        queryset,
                        context={'request': request})
                elif user.groups.all()[0].name == GROUP_RETAIL:
                    queryset = Retail.objects.get(user=user)
                    serializer = RetailSerializer(
                        queryset,
                        context={'request': request})
            except User.DoesNotExist:
                return Response(
                    "User does not exist", status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.all()
            serializer = UserSerializer(
                queryset,
                many=True,
                context={'request': request})
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser, ]


class MallViewSet(viewsets.ModelViewSet):
    queryset = Mall.objects.all()
    serializer_class = MallSerializer
    permission_classes = [IsAdminUser, ]


class RetailViewSet(viewsets.ModelViewSet):
    queryset = Retail.objects.all()
    serializer_class = RetailSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        category = self.request.QUERY_PARAMS.get('category', None)
        location_level = self.request.QUERY_PARAMS.get('location_level', None)
        if category is not None and location_level is not None:
            queryset = Retail.objects.filter(
                category=category,
                location_level=location_level
                )
        elif category is not None:
            queryset = Retail.objects.filter(category=category)
        elif location_level is not None:
            queryset = Retail.objects.filter(location_level=location_level)
        else:
            queryset = Retail.objects.all()
        serializer = RetailSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAuthenticated, ])
    def all_promotions(self, request, pk=None):
        """
        Returns all promotions for a given retailer
        """
        retailer = self.get_object()
        queryset = list(itertools.chain(
            PromotionGeneral.objects.filter(retail=retailer),
            PromotionDiscount.objects.filter(retail=retailer),
            PromotionReduction.objects.filter(retail=retailer),
            ))
        serializer = ReadPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAuthenticated, ])
    def active_promotions(self, request, pk=None):
        """
        Returns active promotions for a given retailer
        """
        retailer = self.get_object()

        # check whether promotion has expired
        now = timezone.make_aware(
            datetime.datetime.now(),
            timezone.get_default_timezone())

        queryset = list(itertools.chain(
            PromotionGeneral.objects.filter(
                retail=retailer,
                time_expiry__gt=now),
            PromotionDiscount.objects.filter(
                retail=retailer,
                time_expiry__gt=now),
            PromotionReduction.objects.filter(
                retail=retailer,
                time_expiry__gt=now),
            ))
        serializer = ReadPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        queryset = list(itertools.chain(
            PromotionGeneral.objects.all(),
            PromotionDiscount.objects.all(),
            PromotionReduction.objects.all(),
            ))
        serializer = ReadPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAdminUser, ])
    def grab_list(self, request, pk=None):
        """
        Returns list of grab promotion entries for a given promotion
        """
        promotion = self.get_object()
        queryset = GrabPromotion.objects.filter(promotion=promotion)
        serializer = GrabPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)


class PromotionReductionViewSet(viewsets.ModelViewSet):
    queryset = PromotionReduction.objects.all()
    serializer_class = PromotionReductionSerializer
    permission_classes = [IsAuthenticated, ]


class PromotionDiscountViewSet(viewsets.ModelViewSet):
    queryset = PromotionDiscount.objects.all()
    serializer_class = PromotionDiscountSerializer
    permission_classes = [IsAuthenticated, ]


class PromotionGeneralViewSet(viewsets.ModelViewSet):
    queryset = PromotionGeneral.objects.all()
    serializer_class = PromotionGeneralSerializer
    permission_classes = [IsAuthenticated, ]


class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(permission_classes=[IsAuthenticated, ])
    def favorite_shops(self, request, pk=None):
        """
        Returns list of favorite retail entries for a given user
        """
        consumer = self.get_object()
        queryset = consumer.favorite_shops.all()
        serializer = RetailSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAuthenticated, ])
    def grab_history(self, request, pk=None):
        """
        Returns list of acknowledged grab promotion entries for a given user
        """
        consumer = self.get_object()
        queryset = GrabPromotion.objects.filter(
            consumer=consumer,
            is_approved=True)
        serializer = ReadGrabPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAuthenticated, ])
    def grab_cart(self, request, pk=None):
        """
        Returns list of pending grab promotion entries for a given user
        """
        consumer = self.get_object()
        queryset = GrabPromotion.objects.filter(
            consumer=consumer,
            is_approved=None)
        serializer = ReadGrabPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)


class GrabPromotionsViewSet(viewsets.ModelViewSet):
    queryset = GrabPromotion.objects.all()
    serializer_class = GrabPromotionSerializer
    permission_classes = [DjangoObjectPermissions, ]

    def get_grab_promotion(self, pk):
        try:
            grab_promotion = GrabPromotion.objects.get(pk=pk)
            return grab_promotion
        except GrabPromotion.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        print(request.user)
        try:
            grab_promotion = self.get_grab_promotion(pk=pk)
            if request.user != grab_promotion.promotion.retail.user:
                return Response(
                    "Current retail has no authority to update this entry.",
                    status=status.HTTP_403_FORBIDDEN)
        except Http404:
            return Response(
                "Entry does not exist",
                status=status.HTTP_404_NOT_FOUND)

        # check whether grab promotion has expired
        now = timezone.make_aware(
            datetime.datetime.now(),
            timezone.get_default_timezone())

        # disable update once:
        # - grab promotion expired, or
        # - approval status has been set
        duration_passed = now > grab_promotion.redeem_time
        if duration_passed or grab_promotion.is_approved is not None:
            return Response(
                "Entry can no longer be modified.",
                status=status.HTTP_406_NOT_ACCEPTABLE)

        # serialize data
        serializer = self.get_serializer(
            grab_promotion,
            data=request.DATA,)
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser, ]
