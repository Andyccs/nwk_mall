from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from nwk.models import Retail,Mall
from django.conf import settings

class Command(BaseCommand):
	def add_retail(self,username,password,email,shop_name,location_level,location_unit):
		retail = User(
			username=username,
			password=password,
			email=email)
		retail.save()
		retail.groups.add(self.retail_group)

		real_retail = Retail(
			user=retail,
			shop_name=shop_name,
			mall=self.mall,
			location_level=location_level,
			location_unit=location_unit)
		real_retail.save()

	def handle(self, **options):

		# Initialize Retail
		retail_list = [
			"Challenger","Channel","Mr.Bean",
			"G2000","Pizza Hut","McDonald's",
			"Subway","Nike","Starbuck"]

		self.mall = Mall(
			mall_name="jurong point",
			address="boonlay MRT",
			region="west",
			redeem_duration=30)
		self.mall.save()

		self.retail_group = Group(name="retail")
		self.retail_group.save()

		for retail in retail_list:
			self.add_retail(retail,retail,retail+"@gmail.com",retail,1,201)
