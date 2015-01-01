from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm
from nwk.models import *


# auto add user to groups on save
@receiver(post_save, sender=Consumer)
def callback_customer_update(sender, instance=None, created=False, **kwargs):
    if created:
        user = instance.user
        user.groups.add(Group.objects.get(name=GROUP_CONSUMER))


@receiver(post_save, sender=Retail)
def callback_retail_update(sender, instance=None, created=False, **kwargs):
    if created:
        perm_add = Permission.objects.get(codename='add_grabpromotion')
        perm_change = Permission.objects.get(codename='change_grabpromotion')
        perm_delete = Permission.objects.get(codename='delete_grabpromotion')
        user = instance.user
        user.user_permissions.add(perm_add, perm_change, perm_delete)
        user.groups.add(Group.objects.get(name=GROUP_RETAIL))


@receiver(post_save, sender=GrabPromotion)
def callback_grab_promo_update(sender, instance=None, created=False, **kwargs):
    if created:
        retail_user = instance.promotion.retail.user
        assign_perm('nwk.change_grabpromotion', retail_user, instance)
        assign_perm('nwk.delete_grabpromotion', retail_user, instance)
