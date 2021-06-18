"""
APIs for create, edit, enable, disable, feedback, and etc will be here

contains:
    createEvent
    editEventImage
    requestedEventList
    searchEvent
    editEventByAdmin
    leaveFeedback
    disableEvent
    userEvent
    deleteEvent
    editEventByUser
    donateMoneyEvent
"""


from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from django.core.paginator import Paginator
from django.db.models import Q

from Backend.settings import HOST, PORT

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event
from App1.models import Transactions
from App1.models import DonatesIn


@api_view(['POST'])
@limiter([CreateEventLimiter])
def createEvent(request):
    """
    potential errors: requiredParams, userNotFound
        ListAndTargetAreNone, MoneyTargetIntError
    """
    try:
        token = request.data["TOKEN_ID"]
        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = get_data_or_none(request, "list_of_needs")
        money_target = get_data_or_none(request, "money_target")
        image_url = get_data_or_none(request, "image_url")
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=token)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=token)
    user = userProfile.user

    if (list_of_needs is None) and (money_target is None):
        return error("ListAndTargetAreNone")

    list_of_needs = [[] if list_of_needs is None else list_of_needs][0]
    needs_string = ""
    for value in list_of_needs:
        needs_string += value + ","
    needs_string = needs_string[:len(needs_string) - 1]

    if money_target is not None:
        try:
            money_target = int(money_target)
        except Exception:
            return error("MoneyTargetIntError")

    Event.objects.create(
        creator=user,
        title=title,
        description=description,
        list_of_needs=needs_string,
        money_target=[money_target if money_target is not None else 0][0],
        image_url=image_url)

    return Response({"message": "event created",
                    "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def editEventImage(request):
    """
    potential errors:, requiredParams, eventNotFound
        userNotFound, notSuperAdmin, eventIsActive
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        event_id = int(request.data["event_id"])
        image_url = request.data["image_url"]
    except Exception:
        return error("requiredParams")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)
    user = userProfile.user

    if user != event.creator:
        if userProfile.user_type not in [1, 2]:
            return error("notSuperAdmin")
        event.image_url = image_url
    else:
        if event.status != 1 and not event.enabled:
            event.image_url = image_url
        else:
            return error("eventIsActive")

    event.save()

    return Response({"message": "event image changed successfully",
                    "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([RequestedEventListLimiter])
def requestedEventList(request):
    """ potential errors: requiredParams, userNotFound, NotSuperAdmin """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type != 1:
        return error("NotSuperAdmin")

    event_set = list(Event.objects.filter(status=0).order_by("-id"))

    return event_lister(event_set)


@api_view(['POST'])
@limiter([SearchLimiter])
def searchEvent(request):
    PAGINATED_BY = 10
    """
    searches for events according to title and description
    just for 'enabled' & 'accepted' events

    potential errors: requiredParams, pageOverFlowError, noResultForSearch
    """
    try:
        search_key = request.data["search_key"]
        page_number = int(request.data["page_number"])
    except Exception:
        return error("requiredParams")

    search_query = Q(title__contains=search_key) | Q(description__contains=search_key)
    allowed_event_query = Q(enabled=1) & Q(status=1)
    result_set = Event.objects.filter(search_query).filter(allowed_event_query).order_by("-id")

    if not len(result_set):
        return error("noResultForSearch")

    # Paginating:
    paginator = Paginator(result_set, PAGINATED_BY)
    if page_number > paginator.num_pages:
        return error("pageOverFlowError", {"the_last_page": paginator.num_pages})
    page = paginator.page(page_number)

    return event_lister(page, pagination_bar_params(page))


@api_view(['POST'])
@limiter([EditEventLimiter])
def editEventByAdmin(request):
    """ potential errors: requiredParams, userNotFound, NotSuperAdminOrAdmin, eventNotFound """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]
        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = request.data["list_of_needs"]
        money_target = int(request.data["money_target"])
        image_url = request.data["image_url"]
        feedback = request.data["feedback"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("NotSuperAdminOrAdmin")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    needs_list = []
    for value in list_of_needs:
        needs_list.append(value)

    event.title = title
    event.description = description
    event.list_of_needs = ",".join(needs_list)
    event.money_target = money_target
    event.image_url = image_url
    event.edited = True
    event.edited_by = userProfile.id
    event.feedback = feedback
    event.status = 1
    event.enabled = True
    event.save()

    return Response({"message": "event edited",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([FeedbackEventLimiter])
def leaveFeedback(request):
    """ potential errors: requiredParams, noSuchUser, notSuperAdminOrAdmin, eventNotFound """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]
        feedback = request.data["feedback"]
        accept = get_data_or_none(request, "accept")

        if accept is None:
            event_status = 0
        elif int(accept) == 1:
            event_status = 1
        else:
            event_status = -1
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("noSuchUser")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    event.feedback = feedback
    event.status = event_status
    event.enabled = [False if accept is None else int(accept)][0]
    event.save()

    return Response({"message": "feedback been leave and status changed",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([DisableEventLimiter])
def disableEvent(request):
    """ potential errors: requiredParams, userNotFound, notSuperAdminOrAdmin, eventNotFound """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    event.enabled = False
    event.save()

    return Response({"message": "event disabled",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([UserEventLimiter])
def userEvent(request):
    """ potential errors: requiredParams, noSuchUser """
    try:
        TOKEN_ID = request.data["token"]
    except Exception:
        return error("requiredParams")

    try:
        userProfile = UserProfile.objects.get(token=TOKEN_ID)
        user = userProfile.user
        eventSet = Event.objects.filter(creator=user).order_by("-id")
        return event_lister(eventSet)
    except Exception:
        return error("noSuchUser")


@api_view(['POST'])
@limiter([DeleteEventByUserLimiter])
def deleteEvent(request):
    """
    delete an event with status 0 by the creator

    potential errors: requiredParams ,eventNotFound
        userNotFound, youAreNotCreator, acceptedEvent
    """
    try:
        event_id = request.data["event_id"]
        TOKEN_ID = request.data["token"]
    except Exception:
        return error("requiredParams")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)
    user = userProfile.user

    if event.creator.username != user.username:
        return error("youAreNotCreator")

    if event.status != 1:
        event.delete()
    else:
        return error("acceptedEvent")

    return Response({"success": "1",
                     "message": "The event deleted successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([EditEventByUserLimiter])
def editEventByUser(request):
    """
    edit event by it's creator according to feedback left by superAdmin

    potential errors: requiredParams, userNotFound
        eventNotFound, youAreNotCreator, rejectedEvent
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]
        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = request.data["list_of_needs"]
        money_target = int(request.data["money_target"])
        image_url = request.data["image_url"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    if event.creator != userProfile.user:
        return error("youAreNotCreator")
    elif event.status == -1:
        return error("rejectedEvent")

    needs_list = []
    for value in list_of_needs:
        needs_list.append(value)

    event.title = title
    event.description = description
    event.list_of_needs = ",".join(needs_list)
    event.money_target = money_target
    event.image_url = image_url
    event.edited = True
    event.edited_by = userProfile.id
    event.status = 0
    event.save()

    return Response({"message": "event edited",
                    "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def donateMoneyEvent(request):
    """
    potential errors: requiredParams, eventNotFound, userNotFound
        userIsNotDonator, userIsNotVerified, eventIsNotEnabled, lessenTheAmount
    """
    try:
        event_id = int(request.data["event_id"])
        TOKEN_ID = request.data["TOKEN_ID"]
        amount = int(request.data["amount"])
    except Exception:
        return error("requiredParams")

    if not len(Event.objects.filter(id=event_id)):
        return error("eventNotFound")
    event = Event.objects.get(id=event_id)

    if not event.enabled:
        return error("eventIsNotEnabled")
    if amount > event.to_money_target():
        return error("lessenTheAmount")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
        return error("userNotFound")
    donator = UserProfile.objects.get(token=TOKEN_ID)

    if donator.user_type not in [1, 3]:
        return error("userIsNotDonator")
    elif not donator.verified:
        return error("userIsNotVerified")

    transaction = Transactions.objects.create(amount=amount,
                                              donatorOrNeedy=donator,
                                              is_in=True)

    DonatesIn.objects.create(transaction=transaction,
                             event=event,
                             donator=donator)
    event.donated_money += amount
    event.save()

    return Response({"message": "money donated successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)
