from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from nwk.models import Retail,Mall,Consumer
from django.conf import settings

class Command(BaseCommand):
	def add_retail(self,
		username,password,email,shop_name,
		location_level,location_unit,logo_url):
		retail = User.objects.create_user(username,email,password)
		retail.save()
		retail.groups.add(self.retail_group)

		real_retail = Retail(
			user=retail,
			shop_name=shop_name,
			mall=self.mall,
			location_level=location_level,
			location_unit=location_unit,
			logo_url=logo_url)
		real_retail.save()

	def add_consumers(self,
		username,password,email):
		consumer = User.objects.create_user(username,email,password)
		consumer.save()
		consumer.groups.add(self.consumer_group)

		real_customer = Consumer(
			user=consumer,
			website="",
			picture="http://twimgs.com/informationweek/galleries/automated/879/01_Steve-Jobs_full.jpg",
			point=0)
		real_customer.save()

	def handle(self, **options):

		# Initialize Retail
		retail_list = [
			{"retail":"Challenger","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-a165def6-f908-43b6-83e8-43264eeb6b4c-challenger.jpg"},
			{"retail":"Channel","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-756a4b0a-7b28-450a-8e38-006fed78ab1f-chanel_logo.gif"},
			{"retail":"Mr.Bean","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-75d1908f-f11d-4ed9-9fa5-089671267c21-1344595157_6.jpg"},
			{"retail":"G2000","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-6f3964d6-ceb5-44d2-beca-c34d4c54389e-g2000.gif"},
			{"retail":"Pizza Hut","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-42718607-4611-40ef-8214-de0354310d88-brand.gif"},
			{"retail":"McDonald's","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-b2aeae9e-0125-4bb1-b35c-541cae843691-6ERHbJBN.jpeg"},
			{"retail":"Subway","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-b37c62a8-3390-4037-827d-e7c07ac10019-Subway-Logo.jpg"},
			{"retail":"Nike","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-d7218c67-06a9-46b9-b15d-ad288a60726d-nike-logo-black.jpg"},
			{"retail":"Starbuck","logo_url":"http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-f08bb1a6-90c9-4607-a971-9fcb167b23e6-starbuck_logo.png"}
			]
		consumer_list = [
			{"username":"andyccs"},
			{"username":"dillon"}
		]

		self.mall = Mall(
			mall_name="jurong point",
			address="boonlay MRT",
			region="west",
			redeem_duration=30)
		self.mall.save()

		self.retail_group = Group(name="retail")
		self.retail_group.save()

		self.consumer_group = Group(name="consumer")
		self.consumer_group.save()

		for retail in retail_list:
			name = retail["retail"]
			logo = retail["logo_url"]
			self.add_retail(name,name,name+"@gmail.com",name,1,201,logo)

		for consumer in consumer_list:
			name = consumer['username']
			self.add_consumers(name,name,name+"@gmail")
