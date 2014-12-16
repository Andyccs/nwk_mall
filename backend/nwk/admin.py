from django.contrib import admin
# Import the UserProfile model individually.
from nwk.models import *


# Register your models here.
admin.site.register(Consumer)
admin.site.register(PromotionGeneral)
admin.site.register(PromotionDiscount)
admin.site.register(Mall)
admin.site.register(Retail)
admin.site.register(GrabPromotion)
