from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *


# API functions:
@api_view(['POST'])
def email(request):
    """
    It's an API to send email from ntm.patronage@gmail.com to a list

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
    except:
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
    except:
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
@limiter([UserEventLimiter])
def userEvent(request):
    """
    passes events created by an specific user

    potential errors:
        requiredParams
        noSuchUser
    """
    try:
        token = request.data["token"]
    except:
        return error("requiredParams")

    try:
        userProfile = UserProfile.objects.get(token=token)
        user = userProfile.user
        eventSet = Event.objects.filter(creator=user)
        return create_event_set(eventSet)
    except:
        return error("noSuchUser")


@api_view(['POST'])
def deleteEvent(request):
    """
    delete an event with status 0 by the creator

    potential errors:
        requiredParams
        noSuchEvent
        noSuchUser
        youAreNotCreator
        acceptedEvent
    """
    try:
        event_id = request.data["event_id"]
        token = request.data["token"]
    except:
        return error("requiredParams")

    try:
        event = Event.objects.get(id=event_id)
    except:
        return error("noSuchEvent")

    try:
        userProfile = UserProfile.objects.get(token=token)
        user = userProfile.user
    except:
        return error("noSuchUser")

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
def editEventByUser(request):
    """
    edit event by it's creator according to feedback left by superAdmin

    potential errors:
        requiredParams
        noSuchUser
        noSuchEvent
        youAreNotCreator
        rejectedEvent
    """
    try:
        token = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]

        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = request.data["list_of_needs"]
        image_url = request.data["image_url"]
    except:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except:
            return error("noSuchUser")

        try:
            event = Event.objects.get(id=event_id)
        except:
            return error("noSuchEvent")
        else:
            if event.creator != userProfile.user:
                return error("youAreNotCreator")
            elif event.status == -1:
                return error("rejectedEvent")

            needs_list = []
            for key, value in list_of_needs.items():
                needs_list.append(value)

            event.title = title
            event.description = description
            event.list_of_needs = ",".join(needs_list)
            event.image_url = image_url
            event.edited = True
            event.edited_by = userProfile.id
            event.status = 0
            event.save()

        return Response({"message": "event edited",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)