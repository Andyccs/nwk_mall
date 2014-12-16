from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from nwk.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from nwk.serializers import *


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


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class PromotionPriceReductionViewSet(viewsets.ModelViewSet):
    queryset = PromotionPriceReduction.objects.all()
    serializer_class = PromotionPriceReductionSerializer


class PromotionPriceDiscountViewSet(viewsets.ModelViewSet):
    queryset = PromotionPriceDiscount.objects.all()
    serializer_class = PromotionPriceDiscountSerializer


class PromotionPriceGeneralViewSet(viewsets.ModelViewSet):
    queryset = PromotionPriceGeneral.objects.all()
    serializer_class = PromotionPriceGeneralSerializer


class ConsumerGeneralViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer


class GrabPromotionsGeneralViewSet(viewsets.ModelViewSet):
    queryset = GrabPromotion.objects.all()
    serializer_class = GrabPromotionSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
