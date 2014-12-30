from django.shortcuts import render_to_response
from django.utils import timezone
from django.http import Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from rest_framework.pagination import PaginationSerializer
from nwk.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope,
                                                 # TokenHasScope
from nwk.serializers import *
import itertools


def register(request):
    '''
    API endpoint for customer registration
    '''
    context = RequestContext(request)

    # A boolean value: whether the registration was successful.
    # Set to False initially. True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Need to set the user attribute ourselves, we set commit=False.
            # Add delay to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update to tell template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    if registered:
        serializer = ConsumerSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered,
        },
        context)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

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
        # TODO: add pagination
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
    permission_classes = [IsAuthenticated, ]

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
    permission_classes = [IsAuthenticated, ]

    def get_grab_promotion(self, pk):
        try:
            grab_promotion = GrabPromotion.objects.get(pk=pk)
            return grab_promotion
        except GrabPromotion.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        try:
            grab_promotion = self.get_grab_promotion(pk=pk)
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
