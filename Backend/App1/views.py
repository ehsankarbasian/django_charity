from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event
from App1.models import Transactions
from App1.models import DonatesIn
from App1.models import Product
from App1.models import NeedRequest

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *
from App1.Components.APIs.store_apis import *
from App1.Components.APIs.transaction_apis import *
from App1.Components.APIs.donate_apis import *
from App1.Components.APIs.need_request_apis import *


# API functions:
@api_view(['POST'])
def email(request):
    """
    It's an API to send email from ntm.patronage@gmail.com to a list
    it can be used by front end too

    potential error:
        requiredParams
    """
    try:
        subject = request.data["subject"]
        message = request.data["message"]
        to_list = request.data["to_list"]
        separated_with = request.data["separated_with"]
        if len(separated_with) == 0:
            separated_with = " "
    except Exception:
        return error("requiredParams")

    to_list = to_list.split(separated_with)
    send_text_email(subject, message, to_list)

    return Response({"message": "email sent",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def promoteToSuperadmin(request):
    try:
        token = request.data["TOKEN_ID"]
        user_id = request.data["user_id"]
    except Exception:
        return error("requiredParams")
    else:
        try:
            adminProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("Wrong TOKEN_ID")
        try:
            userProfile = UserProfile.objects.get(token=user_id)
        except Exception:
            return error("Wrong User_ID")

        # Check whether SuperAdmin or not:
        if adminProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Check user is SuperAdmin or not:
        if userProfile.user_type == 1:
            return error("UserIsSuperAdmin")

        # Promote User To SuperAdmin
        userProfile.user_type = 1
        userProfile.save()

        return Response({"message": "User Promoted To SuperAdmin",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def promoteToAdmin(request):
    try:
        token = request.data["TOKEN_ID"]
        user_id = request.data["user_id"]
    except Exception:
        return error("requiredParams")
    else:
        try:
            adminProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("Wrong TOKEN_ID")
        try:
            userProfile = UserProfile.objects.get(token=user_id)
        except Exception:
            return error("Wrong User_ID")

        # Check whether SuperAdmin or not:
        if adminProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Check user is Admin or not:
        if userProfile.user_type == 2:
            return error("UserIsAdmin")

        # Promote User To SuperAdmin
        userProfile.user_type = 2
        userProfile.save()

        return Response({"message": "User Promoted To Admin",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def demoteAdmin(request):
    try:
        token = request.data["TOKEN_ID"]
        user_id = request.data["user_id"]
        user_type = request.data["user_type"]
    except Exception:
        return error("requiredParams")
    else:
        try:
            adminProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("Wrong TOKEN_ID")
        try:
            userProfile = UserProfile.objects.get(token=user_id)
        except Exception:
            return error("Wrong User_ID")

        # Check whether SuperAdmin or not:
        if adminProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Check user is Admin or not:
        if userProfile.user_type != 1:
            return error("UserIsNotAdmin")

        # Demote User
        userProfile.user_type = user_type
        userProfile.save()

        return Response({"message": "User Demoted",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)
