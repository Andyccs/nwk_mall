from django.contrib import admin
# Import the UserProfile model individually.
from nwk.models import Consumer


# Register your models here.
admin.site.register(Consumer)