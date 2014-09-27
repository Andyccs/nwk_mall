from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Promotion(models.Model):
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=5000)
	quantity = models.PositiveSmallIntegerField() # up to 32767
	time_expiry = models.DateTimeField(auto_now=True) #must be > current time
	image_url = models.CharField(max_length=300)
	created_at = models.DateTimeField(default=datetime.datetime.now())

	def __str__(self):
		return self.title

class PromotionPriceReduction(Promotion):
	original_price = models.DecimalField(max_digits=9, decimal_places=2) # support up to million dollar
	discount_price = models.DecimalField(max_digits=9, decimal_places=2) # support up to million dollar

class PromotionDiscount(Promotion):
	discount = models.PositiveSmallIntegerField()

class PromotionGeneral(Promotion):
	price = models.DecimalField(max_digits=9, decimal_places=2) # support up to million dollar

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.URLField(blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username