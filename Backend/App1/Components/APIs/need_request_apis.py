"""
APIs of needRequests are here

contains:
    createNeedRequest
    requestedNeedRequestList
    myNeedRequestList
    acceptOrRejectNeedRequest
    acceptedNeedRequestList
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
def createNeedRequest(request):
    """ potential errors: requireParams, userNotFound, userTypeError, notVerifiedNeedy """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        title = request.data["title"]
        description = request.data["description"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type != 4:
        return error("userTypeError", {"message": "you are not needy"})
    elif not userProfile.verified:
        return error("notVerifiedNeedy")

    NeedRequest.objects.create(creator=userProfile,
                               title=title,
                               description=description)

    return Response({"message": "NeedRequest created successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def requestedNeedRequestList(request):
    """ potential errors: requiredParams, userNotFound, notSuperAdminOrAdmin """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    needRequest_set = NeedRequest.objects.filter(status=0)

    return needRequest_lister(needRequest_set)


@api_view(['POST'])
def myNeedRequestList(request):
    """ potential errors: requiredParams, userNotFound, userIsNotNeedy """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type == 4:
        needRequestSet = NeedRequest.objects.filter(creator=userProfile)
    else:
        return error("userIsNotNeedy")

    return needRequest_lister(needRequestSet)


@api_view(['POST'])
def acceptOrRejectNeedRequest(request):
    """ potential errors: requiredParams, needRequestNotFound, notSuperAdminOrAdmin, userNotFound """
    try:
        needRequest_id = request.data["NeedRequest_id"]
        TOKEN_ID = request.data["TOKEN_ID"]
        action = bool(request.data["action"])
    except Exception:
        return error("requiredParams")

    if not len(NeedRequest.objects.filter(id=needRequest_id)):
        return error("needRequestNotFound")
    needRequest = NeedRequest.objects.get(id=needRequest_id)

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    needRequest.status = [1 if action else -1][0]
    needRequest.save()

    return Response({"success": "1",
                     "message": "The NeedRequest " + ["accepted" if action else "rejected"][0] + "successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def acceptedNeedRequestList(request):
    count = get_data_or_none(request, "count")
    count = [int(count) if count is not None else 10][0]
    needRequestSet = NeedRequest.objects.filter(status=1)[:count]
    return needRequest_lister(needRequestSet)


@api_view(['POST'])
def allNeedRequestList(request):
    """ potential errors: requiredParams, userNotFound, notSuperAdminOrAdmin """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    needRequest_set = NeedRequest.objects.all()

    return needRequest_lister(needRequest_set)
