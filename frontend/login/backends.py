from django.conf import settings
from django.contrib.auth.models import User, check_password
import requests
import cms_client.settings as settings
import json
import sys
from login.models import Employee

class CustomAuthBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    def authenticate(self, username=None, password=None):
        payload = {'username': username, 'password': password}
        r = requests.post(settings.SERVER_BASE_URL+"auth/login/", data=payload)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            print(r.text)
            if response_dict["result"]=="success":
                token = response_dict["token"]
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # Create a new user. Note that we can set password
                    # to anything, because it won't be checked; the password
                    # from settings.py will.
                    user = User(username=username, password=password)
                    user.is_staff = response_dict["is_staff"]
                    user.is_superuser = response_dict["is_superuser"]
                    user.is_Active = True
                    user.save()
                    employee = Employee(user=user,token=token)
                    employee.save()
                return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None