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
from re import search as validateRegex
from rest_framework import status
from secrets import token_hex

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import ExpiredTokens

from django.test import Client
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def client_post(url, json):
    if url in ['ResetPassword', 'ResetPasswordTokenBased',
               'VerifyEmail', 'VerifyEmailTokenBased']:
        url = "0xAjE2MT6eiOi538574I1NiJ467f4378A9iOiJ821A5IiLC695e6b88FFxkZ1a997F/" + url
    response = Client().post('/App1/' + url, json, format='json')
    return response.data


def client_get():
    # response = Client().get(...)
    pass


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
    EMAIL_REGEX = r'^(\w|\.|\_|\-|\+)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not validateRegex(EMAIL_REGEX, email):
        return {'success': 0}
    try:
        simplified_email = "".join(
            email.split("@")[0]
                .split("+")[0].split(".")
        ) + "@" + email.split("@")[1]

        email_tags_string = "+".join(email.split("@")[0].split("+")[1:])

        return {'success': 1,
                'email': simplified_email,
                'tags': email_tags_string}
    except Exception:
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
    notExpired = True
    for expiredToken in ExpiredTokens.objects.all():
        if token == expiredToken.token:
            notExpired = False

    unique = not bool(len(UserProfile.objects.filter(token=token))) and notExpired

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


def set_email_verified(username):
    """
    set userProfile.verified_email True
    """
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    profile.verified_email = True
    profile.save()


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
