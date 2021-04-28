"""
helper functions are here,
they are not APIs but they help APIs to work
they're imported and used in views.py and *_apis.py
"""


from rest_framework.response import Response
from rest_framework import status
from secrets import token_hex

from App1.models import UserProfile

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def error(message):
    """
    returns error and status-200 and a message
    it's used many times in APIs
    """
    return Response({"status": message,
                     "success": "0"},
                    status=status.HTTP_200_OK)


def simplify_email(email):
    """
    handles dot trick and gmail tags
    doesn't handle wrong format of email
    (it's done in views.py before pass it to this function)
    returns email and tags as strings (tags are '+' joined)
    """
    try:
        simplified_email = "".join(
            email.split("@")[0]
                .split("+")[0].split(".")
        ) + "@" + email.split("@")[1]

        email_tags_string = "+".join(email.split("@")[0].split("+")[1:])

        return {'success': 1,
                'email': simplified_email,
                'tags': email_tags_string}
    except:
        return {'success': 0}


def send_email(subject, message, to_list, html_content):
    """
    Sends html email
    the html_content can have links and etc too
    """
    msg = EmailMultiAlternatives(subject,
                                 message,
                                 settings.EMAIL_HOST_USER,
                                 to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_text_email(subject, message, to_list):
    """
    Sends text email to a list of emails
    there is an API to do so by front
    """
    for email in to_list:
        msg = EmailMultiAlternatives(subject,
                                     message,
                                     settings.EMAIL_HOST_USER,
                                     [email])
        msg.send()


def unique_user_token():
    """
    creates a unique 64-char token for signed up user
    """
    token = token_hex(64)
    unique = not bool(len(UserProfile.objects.filter(token=token)))

    if unique:
        return token
    else:
        unique_user_token()


def get_data_or_none(request, key):
    """
    returns None for not required fields
    """
    try:
        return request.data(key)
    except:
        return None


def create_event_set(event_queryset):
    """
    creates an event_set according to queryset
    it's used in APIs that return several events to front

    the event_set structure is as below:
        {
            "success": "1",
            "event_set": {
                "<<id_of_event>>": {
                    "id", "title", "description", "creator_username", "create_date", "image_url"
                    "list_of_needs":{
                        "1":
                        "2":
                        ...
                        "n":
                    }
                }
            }
        }
    """
    # Create a json for an event:
    event_json = {}
    for event in event_queryset:
        list_of_needs = {}
        if event.list_of_needs is None:
            list_of_needs = ""
        else:
            counter = 0
            for need in event.list_of_needs.split(","):
                counter += 1
                list_of_needs[counter] = need
        user = event.creator
        event_json[event.id] = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "list_of_needs": list_of_needs,
            "creator_username": user.username,
            "create_date": event.create_date,
            "image_url": event.image_url,
        }

    empty = [0 if len(event_json) else 1]
    final_json = {"event_set": event_json, "empty": empty[0], "success": "1"}

    return Response(final_json,
                    status=status.HTTP_200_OK)
