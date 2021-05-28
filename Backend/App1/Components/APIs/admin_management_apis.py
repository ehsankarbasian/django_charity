"""
APIs of adminManagement are here

contains:
    promoteToSuperAdmin
    promoteToAdmin
    demoteAdmin
"""


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from App1.models import *

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *


@api_view(['POST'])
def promoteToSuperAdmin(request):
    """
    promote a user to superAdmin by another superAdmin

    potential errors:
        requiredParams
        superAdminNotFound
        youAreNotSuperAdmin
        userNotFound
        userIsSuperAdmin
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        username = request.data["username"]
    except Exception:
        return error("requiredParams")

    superAdminProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(superAdminProfile):
        return error("superAdminNotFound")
    superAdminProfile = UserProfile.objects.get(token=TOKEN_ID)

    # Check whether SuperAdmin or not:
    if superAdminProfile.user_type != 1:
        return error("youAreNotSuperAdmin")

    user_query = Q(user__username=username)
    userProfile = UserProfile.objects.filter(user_query)
    if not len(userProfile):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(user_query)

    # Check user is SuperAdmin or not:
    if userProfile.user_type == 1:
        return error("userIsSuperAdmin")

    # Promote User To SuperAdmin
    userProfile.user_type = 1
    userProfile.save()

    return Response({"message": "User promoted to SuperAdmin",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def promoteToAdmin(request):
    """
        promote a user to Admin by a superAdmin

        potential errors:
            requiredParams
            superAdminNotFound
            youAreNotSuperAdmin
            userNotFound
            userIsAdmin
            userIsSuperAdmin
        """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        username = request.data["user_id"]
    except Exception:
        return error("requiredParams")

    superAdminProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(superAdminProfile):
        return error("superAdminNotFound")
    superAdminProfile = UserProfile.objects.get(token=TOKEN_ID)

    # Check whether SuperAdmin or not:
    if superAdminProfile.user_type != 1:
        return error("youAreNotSuperAdmin")

    user_query = Q(user__username=username)
    userProfile = UserProfile.objects.filter(user_query)
    if not len(userProfile):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(user_query)

    # Check user is Admin or not:
    if userProfile.user_type == 2:
        return error("userIsAdmin")
    if userProfile.user_type == 1:
        return error("userIsSuperAdmin")

    # Promote User To Admin
    userProfile.user_type = 2
    userProfile.save()

    return Response({"message": "User promoted to Admin",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def demoteAdmin(request):
    """
    promote a user to Admin by a superAdmin

    potential errors:
        requiredParams
        superAdminNotFound
        youAreNotSuperAdmin
        userNotFound
        userIsSuperAdmin
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        username = request.data["username"]
        user_type = int(request.data["user_type"])
    except Exception:
        return error("requiredParams")

    superAdminProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(superAdminProfile):
        return error("superAdminNotFound")
    superAdminProfile = UserProfile.objects.get(token=TOKEN_ID)

    # Check whether SuperAdmin or not:
    if superAdminProfile.user_type != 1:
        return error("youAreNotSuperAdmin")

    user_query = Q(user__username=username)
    userProfile = UserProfile.objects.filter(user_query)
    if not len(userProfile):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(user_query)

    # Check user is Admin or not:
    if userProfile.user_type == 1:
        return error("userIsSuperAdmin")

    # Demote User
    userProfile.user_type = user_type
    userProfile.save()

    return Response({"message": "User Demoted",
                     "success": "1"},
                    status=status.HTTP_200_OK)
