"""
helper functions are here,
they are not APIs but they help APIs to work
they're imported and used in views.py and *_apis.py

contains:
    error
    simplify_email
    send_email
    send_text_email
    unique_user_token
    get_data_or_none

    create_user_items
    create_user_set
    create_event_set

    create_pagination_bar
    pagination_bar_params
"""


import sys

from rest_framework.response import Response
from rest_framework import status
from secrets import token_hex

from App1.models import UserProfile

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def error(message, additional_data=None):
    """
    returns error and status-200 and a message
    it's used many times in APIs

    it can pass additional data too
    additional_data is a dictionary which can be None
    """
    result = {"status": message,
              "error_type": str([[sys.exc_info()[0]] if sys.exc_info()[0] is not None else "CUSTOM"][0]),
              "error_on": str([[sys.exc_info()[1]] if sys.exc_info()[1] is not None else "CUSTOM"][0]),
              "success": "0"}

    if additional_data:
        for key, value in additional_data.items():
            result[key] = value

    return Response(result,
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
    except e:
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
        return request.data[key]
    except Exception:
        return None


# TODO: move to lister_functions.py
def create_user_items(queryset):
    """
    helps the function create_user_set() to not double write the code

    it structs user items in a JSON
    """
    result = {}
    for user in queryset:
        result[user.id] = {
            "id": user.id,
            "username": user.user.username,
            "user_type": user.user_type,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "melli_code": user.melli_code,
            "email": user.email,
            "job": user.job,
            "address": user.address,
            "mobile_number": user.mobile_number,
            "house_phone": user.house_phone,
            "workplace_phone": user.workplace_phone,
            "gender": ["male" if user.gender == 1 else "female"][0],
            "married": user.married,
            "birth_date": user.birth_date,
            "signup_date": user.signup_date,
        }
    return result


# TODO: move to lister_functions.py
def create_user_set(needy_queryset, donator_queryset, pagination_params=None):
    """
    creates json-based user set to show

    the JSON contains: "id", "username", "user_type", "first_name", "last_name",
    "melli_code", "email", "job", "address", "mobile_number", "house_phone",
    "workplace_phone", "gender", "married", "birth_date", "signup_date"

    it gets help from create_user_item() function
    """
    if pagination_params:
        return error("TODO", {"message": "Have no pagination yet; coming soon"})

    needy_json = create_user_items(needy_queryset)
    donator_json = create_user_items(donator_queryset)

    empty_needy = [0 if len(needy_json) else 1]
    empty_donator = [0 if len(donator_json) else 1]

    final_json = {"success": "1",
                  "empty_needy": empty_needy[0],
                  "empty_donator": empty_donator[0],
                  "pagination_params": pagination_params,
                  "needy_set": needy_json,
                  "donator_set": donator_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


# TODO: move to lister_functions.py
def create_event_set(event_queryset, pagination_params=None):
    """
    creates an event_set according to queryset
    it's used in APIs that return several events to front
    it passes pagination params to front if exists too

    the event_set structure is as below:
        {
            "success": "1",
            "empty": "0",
            "pagination_params":{"current_page", "the_last_page", "pagination_bar"}
            "event_set": {
                "<<id_of_event>>": {
                    "status", "id", "title", "description", "list_of_needs", "feedback", "creator_username",
                    "create_date", "image_url", "money_target", "donated_money, "to_money_target"
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
            "status": event.status,
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "list_of_needs": list_of_needs,
            "feedback": [event.feedback if len(event.feedback) else None][0],
            "creator_username": user.username,
            "create_date": event.create_date,
            "image_url": event.image_url,
            "money_target": event.money_target,
            "donated_money": event.donated_money,
            "to_money_target": event.to_money_target(),
        }

    empty = [0 if len(event_json) else 1]
    final_json = {"success": "1",
                  "empty": empty[0],
                  "pagination_params": pagination_params,
                  "event_set": event_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def create_pagination_bar(page):
    """
    returns a ',' separated string according to current_page & number of pages
    the string will be the pagination bar
    """
    paginator = page.paginator
    page_number = page.number
    total_pages = paginator.num_pages

    small_case = bool(total_pages < 10)
    begin_case = bool(page_number <= 5)
    middle_case = bool((page_number > 5) and (page_number < total_pages - 4))
    end_case = bool(page_number >= total_pages - 4)

    pagination_bar = ""
    if small_case:
        for num in range(1, total_pages):
            pagination_bar += str(num)
            pagination_bar += ","
        pagination_bar += str(total_pages)
    elif begin_case:
        for num in range(1, page_number + 3):
            pagination_bar += str(num)
            pagination_bar += ","
        pagination_bar += "...," + str(total_pages - 2) + "," + str(total_pages - 1) + "," + str(total_pages)
    elif middle_case:
        pagination_bar = "1,2,3,...,"
        for num in range(page_number - 2, page_number + 3):
            pagination_bar += str(num)
            pagination_bar += ","
        pagination_bar += "...," + str(total_pages - 2) + "," + str(total_pages - 1) + "," + str(total_pages)
    elif end_case:
        pagination_bar = "1,2,3,...,"
        for num in range(page_number - 2, total_pages + 1):
            pagination_bar += str(num)
            pagination_bar += ","

    return pagination_bar


def pagination_bar_params(page):
    """
    returns parameters of pagination ber to be used in UI
    """

    params = {
        "current_page": page.number,
        "the_last_page": page.paginator.num_pages,
        "pagination_bar": create_pagination_bar(page)
    }
    return params
