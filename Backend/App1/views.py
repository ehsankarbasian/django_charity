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

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *
from App1.Components.APIs.store_apis import *


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
@limiter([SearchLimiter])
def search(request):
    PAGINATED_BY = 10
    """
    searches for events according to title and description
    just for 'enabled' & 'accepted' events
    it's not case-sensitive
    it paginates event by PAGINATED_BY

    potential errors:
        requiredParams
        pageOverFlowError
        noResultForSearch
    """
    try:
        search_key = request.data["search_key"]
        page_number = int(request.data["page_number"])
    except e:
        return error("requiredParams")

    # Search:
    search_query = Q(title__contains=search_key) | Q(description__contains=search_key)
    allowed_event_query = Q(enabled=1) & Q(status=1)
    result_set = Event.objects.filter(search_query).filter(allowed_event_query)

    if not len(result_set):
        return error("noResultForSearch")

    # Paginate:
    paginator = Paginator(result_set, PAGINATED_BY)
    if page_number > paginator.num_pages:
        return error("pageOverFlowError", {"the_last_page": paginator.num_pages})
    page = paginator.page(page_number)

    return create_event_set(page, pagination_bar_params(page))


@api_view(['POST'])
@limiter([NotVerifiedUserSetLimiter])
def notVerifiedUserSet(request):
    """
    returns the list of not verified users to verify by super admin

    potential errors:
        requiredParams
        adminNotFound
        notSuperAdmin
    """
    try:
        TOKEN_API = request.data["TOKEN_API"]
    except Exception:
        return error("requiredParams")

    try:
        adminProfile = UserProfile.objects.get(token=TOKEN_API)
    except Exception:
        return error("adminNotFound")

    if adminProfile.user_type != 1:
        return error("notSuperAdmin")

    donator_list = UserProfile.objects.filter(verified=False).filter(user_type=3)
    needy_list = UserProfile.objects.filter(verified=False).filter(user_type=4)

    return create_user_set(needy_list, donator_list)


@api_view(['POST'])
@limiter([VerifyOrRejectUserLimiter])
def verifyOrRejectUser(request):
    """
    verifies or rejects user by superAdmin

    potential errors:
        requiredParams
        notSuperAdmin
        adminNotFound
        verifiedBefore
        userTypeError
        userNotFound
    """
    try:
        TOKEN_API = request.data["TOKEN_API"]
        user_id = int(request.data["user_id"])
        action = int(request.data["action"])
    except Exception:
        return error("requiredParams")

    try:
        superAdmin = UserProfile.objects.get(token=TOKEN_API)
        if superAdmin.user_type != 1:
            return error("notSuperAdmin")
    except Exception:
        return error("adminNotFound")

    try:
        userProfile = UserProfile.objects.get(id=user_id)
        if userProfile.verified:
            return error("verifiedBefore")
        elif (userProfile.user_type == 1) or (userProfile.user_type == 2):
            return error("userTypeError", {"explanation": "user_type is "
                                                          + str(["superAdmin" if userProfile.user_type == 1 else "admin"][0])})
    except Exception:
        return error("userNotFound")

    if action:
        userProfile.verified = True
        userProfile.save()
    else:
        userProfile.user.delete()
        userProfile.delete()

    return Response({"message": "user " + str(["verified" if action else "rejected (deleted)"][0]) + " successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def donate_money(request):
    """
    donates money for an event

    potential errors:
        requiredParams
        eventNotFound
        userNotFound
        userIsNotDonator
        userIsNotVerified
        eventIsNotEnabled
        lessenTheAmount
    """

    try:
        event_id = int(request.data["event_id"])
        TOKEN_ID = request.data["TOKEN_ID"]
        amount = int(request.data["amount"])
    except Exception:
        return error("requiredParams")

    try:
        event = Event.objects.get(id=event_id)
        if not event.enabled:
            return error("eventIsNotEnabled")
        if amount > event.to_money_target():
            return error("lessenTheAmount")
    except Exception:
        return error("eventNotFound")

    try:
        donator = UserProfile.objects.get(token=TOKEN_ID)
        if donator.user_type not in [1, 3]:
            return error("userIsNotDonator")
        elif not donator.verified:
            return error("userIsNotVerified")
    except Exception:
        return error("userNotFound")

    transaction = Transactions.objects.create(amount=amount,
                                              donatorOrNeedy=donator,
                                              is_in=True)

    DonatesIn.objects.create(transaction=transaction,
                             event=event, donator=donator)
    event.donated_money += amount
    event.save()

    return Response({"message": "money donated successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)
