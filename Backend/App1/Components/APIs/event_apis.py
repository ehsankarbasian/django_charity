"""
APIs for create, edit, enable, disable, feedback, and etc will be here

contains:
    createEvent
    requestedEventList
    editEventByAdmin
    leaveFeedback
    disableEvent
"""


from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event


@api_view(['POST'])
@limiter([CreateEventLimiter])
def createEvent(request):
    """
    creates an event by user with status: 0

    potential errors:
        requiredParams
        Wrong TOKEN_ID
    """
    try:
        token = request.data["TOKEN_ID"]
        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = request.data["list_of_needs"]
        money_target = int(request.data["money_target"])
        image_url = request.data["image_url"]
    except:
        return error("requiredParams")

    # Find user:
    try:
        userProfile = UserProfile.objects.get(token=token)
        user = userProfile.user
    except:
        return error("Wrong TOKEN_ID")

    needs_list = []
    for key, value in list_of_needs.items():
        needs_list.append(value)

    # Create event:
    Event.objects.create(
        creator=user,
        title=title,
        description=description,
        list_of_needs=",".join(needs_list),
        money_target=money_target,
        image_url=image_url
    )

    return Response({"message": "event created",
                    "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([RequestedEventListLimiter])
def requestedEventList(request):
    """
    returns events with status 0 to check by superAdmin

    potential errors:
        requiredParams
        Wrong TOKEN_ID
        NotSuperAdmin
    """
    try:
        token = request.data["TOKEN_ID"]
    except:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except:
            return error("Wrong TOKEN_ID")

        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Find events with status 0:
        event_set = list(Event.objects.filter(status=0))

        return create_event_set(event_set)


@api_view(['POST'])
@limiter([EditEventLimiter])
def editEventByAdmin(request):
    """
    edits event by superAdmin

    potential errors:
        requiredParams
        Wrong TOKEN_ID
        NotSuperAdmin
        WrongEventId
    """
    try:
        token = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]

        title = request.data["title"]
        description = request.data["description"]
        list_of_needs = request.data["list_of_needs"]
        money_target = int(request.data["money_target"])
        image_url = request.data["image_url"]
        feedback = request.data["feedback"]
    except:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except:
            return error("Wrong TOKEN_ID")

        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Edit event:
        try:
            event = Event.objects.get(id=event_id)
        except:
            return error("WrongEventId")
        else:
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
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([FeedbackEventLimiter])
def leaveFeedback(request):
    """
    leave a feedback for an event by superAdmin
    front email it to user too

    potential errors:
        requiredParams
        noSuchUser
        NotSuperAdmin
        EventDoesNotExist
    """
    try:
        token = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]

        feedback = request.data["feedback"]
        accept = get_data_or_none(request, "accept")
        if accept is None:
            event_status = 0
        elif int(accept) == 1:
            event_status = 1
        else:
            event_status = -1

    except:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except:
            return error("noSuchUser")
        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Leave feedback for the event:
        try:
            event = Event.objects.get(id=event_id)
        except:
            return error("EventDoesNotExist")
        else:
            event.feedback = feedback
            event.status = event_status
            event.enabled = [False if accept is None else int(accept)][0]
            event.save()

        return Response({"message": "feedback been leave and status changed",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([DisableEventLimiter])
def disableEvent(request):
    """
    disable an event (expire event) by superAdmin

    potential errors:
        requiredParams
        Wrong TOKEN_ID
        NotSuperAdmin
    """
    try:
        token = request.data["TOKEN_ID"]
        event_id = request.data["event_id"]
    except:
        return error("requiredParams")
    else:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except:
            return error("Wrong TOKEN_ID")

        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Disable the event:
        event = Event.objects.get(id=event_id)
        event.enabled = False
        event.save()

        return Response({"message": "event disabled",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


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
        money_target = int(request.data["money_target"])
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
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)
