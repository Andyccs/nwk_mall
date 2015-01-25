from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from nwk.models import Retail, Mall, Consumer, PromotionReduction, PromotionDiscount, PromotionGeneral
from django.conf import settings
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application


CAT_FOOD = 'FOOD'
CAT_FASHION = 'FASHION'
CAT_LIFESTYLE = 'LIFESTYLE'
CAT_OTHER = 'OTHER'

OAUTH_TEST_ID = "kF0oFIZP7@uiMABQzHLirc8q8hUsz!F!peyUJEV;"
OAUTH_TEST_SECRET ="umK2JXvw?LcDH@KX?5!c8yjBtz-2caNiTLoB6ij6keIYAQEI39UGtv6qaRyuAI8L0wWS9E8!cy!btNxdUIiqZ?1SGcpSv9?jTyjnm;csarQuOpbai3Ccc.th2=G_YVFg"

class Command(BaseCommand):
    def add_application(self, user,
        client_id='', client_secret='',
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD):
        if client_id and client_secret:
            Application.objects.create(
                user=user,
                client_id=client_id,
                client_secret=client_secret,
                client_type=client_type,
                authorization_grant_type=authorization_grant_type)
        else:
            Application.objects.create(
                user=user,
                client_type=client_type,
                authorization_grant_type=authorization_grant_type)

    def add_retail(self,
        username, password, email, shop_name, 
        location_level, location_unit, logo_url, category):
        retail = User.objects.create_user(username, email, password)
        retail.save()
        retail.groups.add(self.retail_group)

        real_retail = Retail(
            user=retail,
            shop_name=shop_name,
            mall=self.mall,
            category=category,
            location_level=location_level,
            location_unit=location_unit,
            logo_url=logo_url)
        real_retail.save()
        return real_retail

    def add_consumers(self,
        username, password, email):
        consumer = User.objects.create_user(username,email,password)
        consumer.save()
        consumer.groups.add(self.consumer_group)

        real_customer = Consumer(
            user=consumer,
            picture="http://twimgs.com/informationweek/galleries/automated/879/01_Steve-Jobs_full.jpg",
            point=0)
        real_customer.save()

    def handle(self, **options):

        # Initialize Retail
        retail_list = [
            {
                "retail": "Challenger",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-a165def6-f908-43b6-83e8-43264eeb6b4c-challenger.jpg",
                "category": CAT_LIFESTYLE,
                "promotions":[
                    {
                        "title": "Pax 9-Course Chinese",
                        "description": "Ah Yat Five Treasure Combination. Bird’s Nest with Winter Melon Thick Soup. Stewed Abalone with Mushroom wrapped in Zucchini. Braised Wild Duck with Sea Cucumber. “Hakka” Style Yong Tau Foo. Poached Bean Curd Roll with Three Types Egg. Deep-Fried Soon Hock Fish in HK Style. Grandma Fried Rice. Yam Paste with Red Bean and Coconut Milk. Authentic Hong Kong-style cuisine. Esteemed team of chefs with over 20 years’ experience. Located at The Village @ Jurong Hill, a short walk away from Jurong Bird Park. Parking available at $2 per entry from 8am to 5pm, and is complimentary after 5pm",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-999954fa-3a70-4d65-8728-46170af00865-tfss-45452756-2d5d-4cdd-9cd5-d72c39843afc-1412699486630.jpg",
                        "original_price":259.9,
                        "discount_price":149.8
                    },
                    {
                        "title": "Pampering Nails Hen's Party",
                        "description": "Each person has a choice of either a gel mani or a classic mani pedi. File and trim nails into perfection neatly. Achieve longer-lasting gel manicure polished nails infused with collagen soft gel polishes. Disinfectant Spray. Sea Salt Anti Bacterial Foot Soak(pedi). Choice of 1 colour nail polish/gel polish. Hand moisturising massage. Great bonding sessions celebrating birthdays, hens party and get-togethers. Botanical inhouse quality Nfu.Oh nail polishes available. Over 500 colours to choose in different finishes. Modern and comfortable nail boutique. Cushy and lush decor. Located 3 mins away from Holland Village MRT CC21",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-c541296d-1a37-4fe3-b82e-3e7c821e1361-tfss-51ae7b9b-cdfc-4235-8d05-e1e6ebd441af-1407813317342.jpg",
                        "original_price":384,
                        "discount_price":72
                    }
                ]
                },
            {
                "retail": "Channel",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-756a4b0a-7b28-450a-8e38-006fed78ab1f-chanel_logo.gif",
                "category": CAT_FASHION,
                "promotions": [
                    {
                        "title": "Young Hearts Cash Voucher",
                        "description": "Bras, panties, nighties, and training bras in various colours and designs. Cash vouchers can be combined for more value and are valid with existing promotions. CapitaVoucher can be used with Young Hearts cash voucher. CapitaVoucher can be used at all participating stores and is valid till Aug 31, 2015. Young Hearts Cash Voucher is valid till Dec 31, 2014.",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-b9d19833-a653-4045-885d-3d82d939ba4d-tfss-aefa1319-2860-4179-b257-f662b3537e7c-1413795418588.jpg",
                        "price":20
                    },
                    {
                        "title": "Chanel Caviar Flap Handbag",
                        "description": "Luxurious, statement making classic from Chanel. Signature quilted design and gold chains. Highly coveted design. Made with premium caviar calfskin. Great as a gift or personal treat. Chanel Care Booklet. Dust Bag. Authenticity Card. Box. Limited Groupons available",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-3a9813e4-3e01-41f4-8e6a-629a071a0648-1414046000779.jpg",
                        "original_price":8410,
                        "discount_price":7779
                    }
                ]
            },
            {
                "retail": "Mr.Bean",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-75d1908f-f11d-4ed9-9fa5-089671267c21-1344595157_6.jpg",
                "category": CAT_FOOD,
                "promotions": [
                    {
                        "title": "Classic Icy Soya Milk",
                        "description": "Come try our Classic Icy Soya Milk with a CITRUS-y twist! Quench your thirst with this refreshing classic drink, filled with bursting calamansi and pineapple pops! Get it at $2.50 (16 oz) at our stores! Hurry, limited period only!",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-8a5f98d8-6a05-4548-91f7-f6e7a61baa2d-10678632_567482453397384_3984868414334754337_n.png",
                        "original_price":5,
                        "discount_price":2.5
                    }
                ]
            },
            {
                "retail": "G2000",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-6f3964d6-ceb5-44d2-beca-c34d4c54389e-g2000.gif",
                "category": CAT_FASHION,
                "promotions": [
                    {
                        "title": "Xiaomi 10400mAh Powerbank",
                        "description": "Powered by the latest battery technology from LG and Samsung. Sleek, minimalist and compact design. Dedicated thermostat ensures cells are always working at a safe temperature. Circuit breaker to prevent further damage should short circuiting occur. If changes in the surrounding environment cause MI Charger to stop functioning, just tap the power button to reset the charger and continue charging. Voltage input limit protects cells from being charged with too much voltage. Feedback protection; charger stops automatically to prevent damage to your device in case of USB output being plugged accidentally into power source. Device detection automatically checks for live power current when connected to a device. Voltage output limit; actively checks to ensure that voltage output to charging devices is kept at a safe and constant rate. Charge limit helps to maximize your devices’ battery usage life. PTC protection controls the flow of voltage and protect the battery cells in case of charger overheating with excessive voltage released. Micro USB Cable. User manual. 3 months local agent warranty (see Fine Print for more details)",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-1e00473e-0a9e-4f6f-9f8d-e0a2831a3ad6-1413510147013.jpg",
                        "original_price": 29.9,
                        "discount_price": 17.5
                    }
                ]
                },
            {
                "retail": "Pizza Hut",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-42718607-4611-40ef-8214-de0354310d88-brand.gif",
                "category": CAT_FOOD,
                "promotions": [
                    {
                        "title": "Hand Stretched Thin Pizza",
                        "description": "Up to 12 toppings to choose from. Applicable for Pan/ Hand Stretched Thin pizza except for Signature Series. Valid at Pizza Hut Dine-In Restaurants except NTU, ARC and The Signature.",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-a171f69d-fd0e-4d54-b5bf-85fad28e0ee2-1413872193637.jpg",
                        "original_price": 30.65,
                        "discount_price": 14.5
                    }
                ]
                },
            {
                "retail": "McDonald's",
                "level":1,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-b2aeae9e-0125-4bb1-b35c-541cae843691-6ERHbJBN.jpeg",
                "category": CAT_FOOD,
                "promotions": []
                },
            {
                "retail": "Subway",
                "level":2,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-b37c62a8-3390-4037-827d-e7c07ac10019-Subway-Logo.jpg",
                "category": CAT_FOOD,
                "promotions": [
                    {
                        "title": "$5 Fresh Value Combos",
                        "description": "5 Combos, Everyday. All combos come with a 6-inch sub & 16oz drink",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-8f53c68f-ebb6-402e-a6a8-5580d2b2e032-newsbites6big.jpg",
                        "discount": 10
                    }
                ]
                },
            {
                "retail": "Nike",
                "level":2,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-d7218c67-06a9-46b9-b15d-ad288a60726d-nike-logo-black.jpg",
                "category": CAT_LIFESTYLE,
                "promotions": []
            },
            {
                "retail": "Starbuck",
                "level":2,
                "logo_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-f08bb1a6-90c9-4607-a971-9fcb167b23e6-starbuck_logo.png",
                "category": CAT_FOOD,
                "promotions":[
                    {
                        "title": "Frappuccino",
                        "description": "Add a shot of espresso, include some sweet syrup or even switch your milk to soy. Personalize your handcrafted drink with 1 free customization. Simply mention “Facebook Treats” at the counter.",
                        "image_url": "http://files.parsetfss.com/ba2cde20-dd78-4c86-9bda-e4db4bf2b973/tfss-0de77848-18ef-43ed-a8dc-84b0e1bd59dd-caramel-frappuccino-51087.jpg",
                        "discount": 20
                    }
                ]
                }
            ]
        consumer_list = [
            {"username": "andyccs"},
            {"username": "dillon"}
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
            category = retail["category"]
            level = retail["level"]
            real_retail = self.add_retail(name, name, name+"@gmail.com", name,
                                          level, 201, logo, category)
            for promotion in retail['promotions']:
                if(promotion.get("original_price")):
                    p = PromotionReduction(
                        retail=real_retail,
                        title=promotion["title"],
                        description=promotion["description"],
                        image_url=promotion["image_url"],
                        original_price=promotion["original_price"],
                        discount_price=promotion["discount_price"]
                        )
                    p.save()
                elif(promotion.get("discount")):
                    p = PromotionDiscount(
                        retail=real_retail,
                        title=promotion["title"],
                        description=promotion["description"],
                        image_url=promotion["image_url"],
                        discount=promotion["discount"]
                        )
                    p.save()
                elif(promotion.get("price")):
                    p = PromotionGeneral(
                        retail=real_retail,
                        title=promotion["title"],
                        description=promotion["description"],
                        image_url=promotion["image_url"],
                        price=promotion["price"]
                        )
                    p.save()

        for consumer in consumer_list:
            name = consumer['username']
            self.add_consumers(name, name, name+"@gmail")

        #Create super user
        self.UserModel = get_user_model()
        user_data = {}
        user_data['username'] = 'admin'
        user_data['password'] = 'admin'
        user_data['email']='admin@example.com'
        admin = self.UserModel._default_manager.db_manager("default").create_superuser(**user_data)
        
        # create oauth application
        self.add_application(
            user=admin, client_id=OAUTH_TEST_ID,
            client_secret=OAUTH_TEST_SECRET)
