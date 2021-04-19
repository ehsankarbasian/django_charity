from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from App1.models import UserProfile

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from re import search as validateRegex
from secrets import token_hex
from App1.custom_limiter import *

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

# TODO: delete it
from django.http import HttpResponse

# Statics:
from Backend.urls import TOKEN_API, EMAIL_TOKEN_API
HOST = '127.0.0.1'
PORT = '8000'
EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


# Helper functions:
def error(message):
    return Response({"status": message,
                     "success": "0"},
                    status=status.HTTP_200_OK)


def simplify_email(email):
    try:
        # Handle email tags and dot trick:
        email_tags_string = "+".join(email.split("@")[0].split("+")[1:])
        simplified_email = "".join(
            email.split("@")[0]
                .split("+")[0].split(".")
        ) + "@" + email.split("@")[1]

        return {'success': 1,
                'email': simplified_email,
                'tags': email_tags_string}
    except:
        return {'success': 0}


def get_data_or_none(request, key):
    try:
        return request.data(key)
    except:
        return None


# API functions:
@api_view(['POST'])
@limiter([LoginLimiter])
def login(request):
    if request.session.get('user_id', None) is not None:
        return error("loggedInBefore")
    try:
        username = request.data["username"]
        password = request.data["password"]
    except:
        return error("requiredParams")
    else:
        user = authenticate(
            username=username,
            password=password
        )
        if user is None:
            return error("wrongUsernameOrPass")
        else:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)

            # Check verified_email:
            if not user_profile.verified_email:
                return error("emailVerificationError")

            request.session['user_id'] = user.id
            return Response({"username": user.username,
                             "email": user_profile.email,
                             "user_type": user_profile.user_type,
                             "success": "1"},
                            status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SignUpLimiter])
def signup(request):
    try:
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        user_type = int(request.data["user_type"])
    except:
        return error("requiredParams")
    else:
        original_email = email
        result = simplify_email(original_email)
        if not result['success']:
            return error("invalidEmailError")
        email = result['email']
        email_tags_string = result['tags']

        # Validate email using regex:
        if not validateRegex(EMAIL_REGEX, email):
            return error("invalidEmailError")

        # Handle before-used username or emails or Both:
        username_error = len(User.objects.filter(username=username))
        email_error = len(User.objects.filter(email=original_email)) \
                      + len(User.objects.filter(email=email))
        if username_error and email_error:
            # before-used username and email:
            return error("emailUsernameError")
        elif username_error:
            # before-used username:
            return error("usernameError")
        elif email_error:
            # before-used email:
            return error("emailError")

        elif user_type not in [3, 4]:
            return error("notAllowedUserTypeError")

        else:
            user = User.objects.create_user(
                username=username,
                email=original_email,
                password=password
            )
            UserProfile.objects.create(
                user=user,
                email=email,
                email_tags=email_tags_string,
                user_type=user_type
            )
            return Response({"username": username,
                             "email": email,
                             "user_type": user_type,
                             "success": "1"},
                            status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ForgotPasswordLimiter])
def forgotPassword(request):
    try:
        email = request.data["email"]
    except:
        return error("RequiredParams")

    email = simplify_email(email)

    if not email['success']:
        return error("invalidEmailError")

    to_email = email['email']

    # Check if email verified:
    user = UserProfile.objects.get(email=to_email)
    if user is None:
        return error("noSuchUser")
    elif not user.verified_email:
        return error("notVerifiedEmailError")

    # TODO:create token and link and send email
    token = token_hex(128)
    user.reset_pass_token = token
    user.save()

    html_content = get_template('ResetPass.html').render(context={
        'HOST': HOST,
        'PORT': PORT,
        'EMAIL_TOKEN_API': EMAIL_TOKEN_API,
        'email': to_email,
        'private_token': token
    })
    msg = EmailMultiAlternatives('charity reset password',
                                 'message',
                                 settings.EMAIL_HOST_USER,
                                 ['ehsankarbasian@gmail.com'])  # <---- TODO: change the email to [to_email]
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response({"success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@limiter([ResetPasswordLimiter])
def resetPassword(request):
    pass1 = request.POST["pass1"]
    pass2 = request.POST["pass2"]

    token = request.POST["token"]
    email = request.POST["email"]

    if pass1 != pass2:
        return error("differentPasswords")

    # Find user:
    userProfile = UserProfile.objects.get(email=email)
    user = User.objects.get(user=userProfile)

    # Check token:
    if not userProfile.reset_pass_token == token:
        return error("privateTokenError")

    # Change private token and password
    userProfile.reset_pass_token = token_hex(64)
    userProfile.save()
    user.set_password(pass1)
    user.save()

    return Response({"success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@limiter([LogOutLimiter])
def logout(request):
    if request.session.get('user_id', None) is None:
        return error("notLoggedIn")
    try:
        request.session['user_id'] = None
        return Response({"success": "1"},
                        status=status.HTTP_200_OK)
    except:
        return error("unsuccessfulLogout")


@api_view(['POST'])
@limiter([LoadProfileLimiter])
def loadUserProfile(request):
    try:
        if not request.session.get('user_id', False):
            return error("notLoggedIn")
        username = request.data["username"]
    except:
        return error("requiredParams")

    try:
        user_id = request.session.get('user_id', 0)
        user = User.objects.get(id=user_id)
        if username != user.username:
            print(request.user.is_authenticated)
            # current_user in backend is different with current_user.username sent form frontend.
            return error("differentUsername")
        current_user = UserProfile.objects.get(user=user)
    except:
        return error("DoesNotExist")
    else:
        # Send current_user.details to front:
        return Response({"username": username,
                         "user_type": current_user.user_type,
                         "first_name": current_user.first_name,
                         "last_name": current_user.last_name,
                         "melli_code": current_user.melli_code,
                         "email": current_user.email,
                         "job": current_user.job,
                         "address": current_user.address,
                         "mobile_number": current_user.mobile_number,
                         "house_phone": current_user.house_phone,
                         "workplace_phone": current_user.workplace_phone,
                         "gender": current_user.gender,
                         "married": current_user.married,
                         "birth_date": current_user.birth_date,
                         "verified_needy": current_user.verified_needy,
                         "verified_mobile": current_user.verified_mobile,
                         "verified_email": current_user.verified_email,
                         "is_profile_completed": current_user.completed,
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SubmitProfileLimiter])
def submitUserProfile(request):
    if not request.session.get('user_id', False):
        return error("notLoggedIn")

    try:
        # Required fields:
        username = request.data["username"]
        user_type = request.data["user_type"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        melli_code = request.data["melli_code"]
        mobile_number = request.data["mobile_number"]
    except:
        return error("requiredParams")
    else:
        # Check user:
        user = get_object_or_404(User, username=username)
        userProfile = get_object_or_404(UserProfile, user=user)
        valid_user = bool(request.session.get('user_id', None) == user.id)
        valid_type = bool(userProfile.user_type == user_type)
        if not (valid_user and valid_type):
            return error("DisputeError")

        # NOT required fields:
        job = get_data_or_none(request, "job")
        address = get_data_or_none(request, "address")
        house_phone = get_data_or_none(request, "house_phone")
        workplace_phone = get_data_or_none(request, "workplace_phone")
        gender = get_data_or_none(request, "gender")
        married = get_data_or_none(request, "married")
        birth_date = get_data_or_none(request, "birth_date")

        # Update User:
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update UserProfile:
        userProfile = UserProfile.objects.get(user=user)
        userProfile.first_name = first_name
        userProfile.last_name = last_name
        userProfile.melli_code = melli_code
        userProfile.mobile_number = mobile_number
        userProfile.gender = gender
        userProfile.job = job
        userProfile.address = address
        userProfile.house_phone = house_phone
        userProfile.workplace_phone = workplace_phone
        userProfile.married = married
        userProfile.birth_date = birth_date

        userProfile.completed = True
        userProfile.save()

        return Response({"username": username,
                         "email": userProfile.email,
                         "user_type": user_type,
                         "success": "1"},
                        status=status.HTTP_200_OK)
