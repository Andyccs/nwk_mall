from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from nwk.models import *


# auto add user to groups on save
@receiver(post_save, Consumer)
def callback_customer_update(sender, instance=None, created=False, **kwargs):
    if created:
        user = instance.user
        user.groups.add(Group.objects.get(name=GROUP_CONSUMER))


@receiver(post_save, Retail)
def callback_retail_update(sender, instance=None, created=False, **kwargs):
    if created:
        user = instance.user
        user.groups.add(Group.objects.get(name=GROUP_RETAIL))
