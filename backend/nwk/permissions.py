from nwk.models import *
from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """

    def has_object_permission(self, request, view, obj):
        # check if user is owner
        return request.user == obj


class GrabPromotionPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        retail = obj.promotion.retail
        consumer = obj.consumer
        # check if user is owner
        is_owned = request.user == retail.user or request.user == consumer.user
        print(str(retail))
        print(str(consumer))
        print(str(request.user))
        return is_owned
