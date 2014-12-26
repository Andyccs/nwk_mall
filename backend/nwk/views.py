from django.shortcuts import render_to_response
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext
from nwk.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from nwk.serializers import *
import itertools


# TODO: add method to get promotion from all 3 tables
# def get_all_promotions(retail=None):
#     if retail:
#         pass
#     else:
#         p_discount = PromotionDiscount.objects.all()
#         p_general = PromotionGeneral.objects.all()
#     p_discount_serializer = PromotionDiscountSerializer(p_discount)
#     p_general_serializer = PromotionGeneralSerializer(p_general)
#     promotions = []
#     promotions += p_discount_serializer.data
#     return Response()


def index(request):
    return HttpResponse("Hello, world. You're at the nwk index.\n")


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
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

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
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

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
        {'user_form': user_form,
         'profile_form': profile_form,
         'registered': registered},
        context)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MallViewSet(viewsets.ModelViewSet):
    queryset = Mall.objects.all()
    serializer_class = MallSerializer


class RetailViewSet(viewsets.ModelViewSet):
    queryset = Retail.objects.all()
    serializer_class = RetailSerializer

    def list(self, request):
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = Retail.objects.filter(category=category)
        else:
            queryset = Retail.objects.all()
        serializer = RetailSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)

    @detail_route()
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

    @detail_route()
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


# class PromotionTypeViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PromotionType.objects.all()
#     serializer_class = PromotionTypeSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

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

    @detail_route()
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


class PromotionDiscountViewSet(viewsets.ModelViewSet):
    queryset = PromotionDiscount.objects.all()
    serializer_class = PromotionDiscountSerializer


class PromotionGeneralViewSet(viewsets.ModelViewSet):
    queryset = PromotionGeneral.objects.all()
    serializer_class = PromotionGeneralSerializer


class ConsumerGeneralViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

    @detail_route()
    def grab_history(self, request, pk=None):
        """
        Returns list of grab promotion entries for a given user
        """
        consumer = self.get_object()
        queryset = GrabPromotion.objects.filter(
            consumer=consumer,
            is_approved=True)
        serializer = GrabPromotionSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data)


class GrabPromotionsGeneralViewSet(viewsets.ModelViewSet):
    queryset = GrabPromotion.objects.all()
    serializer_class = GrabPromotionSerializer

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

        # disable update once grab promotion expired
        duration_passed = now > grab_promotion.redeem_time
        if duration_passed:
            return Response(
                "Grab Promotion has Expired",
                status=status.HTTP_406_NOT_ACCEPTABLE)

        # serialize data
        serializer = self.get_serializer(
            grab_promotion,
            data=request.DATA,
            context={'request': request})
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
