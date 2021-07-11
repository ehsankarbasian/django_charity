"""
APIs of adminManagement are here

contains APIs:
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


def checkSuperAdminOrNot(request):
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        username = request.data["username"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("superAdminNotFound")
    superAdminProfile = UserProfile.objects.get(token=TOKEN_ID)

    if superAdminProfile.user_type != 1:
        return error("youAreNotSuperAdmin")

    return username


def generalPromote(username, user_type):
    user_query = Q(user__username=username)
    if not len(UserProfile.objects.filter(user_query)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(user_query)

    if (userProfile.user_type == 2) and (user_type == 2):
        return error("userIsAdmin")
    if userProfile.user_type == 1:
        return error("userIsSuperAdmin")

    userProfile.user_type = user_type
    userProfile.save()

    return Response({"message": "User promoted to " + ["Admin" if user_type == 2 else "superAdmin"][0],
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def promoteToSuperAdmin(request):
    """
    potential errors: requiredParams, superAdminNotFound
        youAreNotSuperAdmin, userNotFound, userIsSuperAdmin
    """
    username = checkSuperAdminOrNot(request)
    if str(type(username)) == "<class 'rest_framework.response.Response'>":
        return username
    else:
        return generalPromote(username, 1)


@api_view(['POST'])
def promoteToAdmin(request):
    """
    potential errors: requiredParams, superAdminNotFound
        youAreNotSuperAdmin, userNotFound, userIsAdmin, userIsSuperAdmin
    """
    username = checkSuperAdminOrNot(request)
    if str(type(username)) == "<class 'rest_framework.response.Response'>":
        return username
    else:
        return generalPromote(username, 2)


@api_view(['POST'])
def demoteAdmin(request):
    """
    demote Admin to donator or needy by superAdmin

    potential errors: requiredParams, superAdminNotFound, youAreNotSuperAdmin
        userNotFound, userIsSuperAdmin, userIsDonator, userIsNeedy, dontDemoteToSuperAdmin
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        username = request.data["username"]
        user_type = int(request.data["user_type"])
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("superAdminNotFound")
    superAdminProfile = UserProfile.objects.get(token=TOKEN_ID)

    if superAdminProfile.user_type != 1:
        return error("youAreNotSuperAdmin")

    user_query = Q(user__username=username)
    if not len(UserProfile.objects.filter(user_query)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(user_query)

    if userProfile.user_type == 1:
        return error("userIsSuperAdmin")
    elif userProfile.user_type == 3:
        return error("userIsDonator")
    elif userProfile.user_type == 4:
        return error("userIsNeedy")

    if user_type == 1:
        return error("dontDemoteToSuperAdmin")
    userProfile.user_type = user_type
    userProfile.save()

    return Response({"message": "User Demoted",
                     "success": "1"},
                    status=status.HTTP_200_OK)
