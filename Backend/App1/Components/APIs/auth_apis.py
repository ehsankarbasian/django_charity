"""
APIs of auth and reset-pass, will be here

contains:
    login
    signup
    logout

    verifyEmailTokenBased
    verifyEmailCodeBased

    forgotPassword
    resetPasswordTokenBased
    resetPasswordCodeBased

    notVerifiedUserSet
    verifyOrRejectUser
"""

from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.template.loader import get_template

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *
from re import search as validateRegex
from random import randint

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import ExpiredTokens

from Backend.urls import TOKEN_API, EMAIL_TOKEN_API, HOST, PORT

EMAIL_REGEX = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


@api_view(['POST'])
@limiter([LoginLimiter])
def login(request):
    """
    user login in sessions and pass a token to front

    potential errors:
        requiredParams
        wrongUsernameOrPass
        emailVerificationError
    """
    try:
        username = request.data["username"]
        password = request.data["password"]
    except Exception:
        return error("requiredParams")
    else:
        # Authenticate:
        user = authenticate(
            username=username,
            password=password
        )
        if user is None:
            return error("wrongUsernameOrPass")

        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        # Check verified_email:
        if not user_profile.verified_email:
            return error("emailVerificationError")

        request.session['user_id'] = user.id
        return Response({"username": user.username,
                         "email": user_profile.email,
                         "token": user_profile.token,
                         "user_type": user_profile.user_type,
                         "success": "1"},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SignUpLimiter])
def signup(request):
    """
    user signup according to user_type
    just to signup as donator or needy
    emails to user to verify it

    potential errors:
        requiredParams
        invalidEmailError
        emailUsernameError
        usernameError
        emailError
        notAllowedUserTypeError
    """
    try:
        username = request.data["username"]
        original_email = request.data["email"]
        password = request.data["password"]
        user_type = int(request.data["user_type"])
    except Exception:
        return error("requiredParams")
    else:
        simple_email_set = simplify_email(original_email)
        if not simple_email_set['success']:
            return error("invalidEmailError")
        simple_email = simple_email_set['email']
        email_tags_string = simple_email_set['tags']

        # Validate email using regex:
        if not validateRegex(EMAIL_REGEX, simple_email):
            return error("invalidEmailError")

        # Handle before-used username or emails or Both:
        username_error = len(User.objects.filter(username=username))
        email_error = bool(len(User.objects.filter(email=original_email))
                           or len(User.objects.filter(email=simple_email)))
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
            verify_email_code = randint(100000, 999999)
            verify_email_token = token_hex(64)
            token = unique_user_token()

            user = User.objects.create_user(
                username=username,
                email=original_email,
                password=password
            )
            UserProfile.objects.create(
                user=user,
                email=simple_email,
                token=token,
                email_tags=email_tags_string,
                user_type=user_type,
                verify_email_code=verify_email_code,
                verify_email_token=verify_email_token
            )

            # Sending html based email to user to verify his/her email:
            html_content = get_template('EmailVerification.html').render(context={
                'HOST': HOST,
                'PORT': PORT,
                'EMAIL_TOKEN_API': EMAIL_TOKEN_API,
                'email': simple_email,
                'name': username,
                'private_code': verify_email_code,
                'private_token': verify_email_token
            })
            send_email(subject='NTM charity email verification',
                       message='Email verification',
                       to_list=[simple_email],
                       html_content=html_content)

            return Response({"username": username,
                             "email": simple_email,
                             "user_type": user_type,
                             "success": "1"},
                            status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([LogOutLimiter])
def logout(request):
    """
    logs out user from sessions
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    userProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(userProfile):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    ExpiredTokens.objects.create(token=TOKEN_ID)

    userProfile.token = unique_user_token()
    userProfile.save()

    return Response({"message": "successfully logged out",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SignUpLimiter])
def verifyEmailTokenBased(request):
    """
    verifies email using the link sent in email

    potential errors:
        requiredParams
        privateTokenError
    """
    try:
        private_token = request.data["token"]
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    userProfile = UserProfile.objects.get(email=email)
    if userProfile.verify_email_token == private_token:
        userProfile.verified_email = True
        userProfile.save()
        return Response({"message": "email verification was successful, you can login now!",
                         "success": "1"},
                        status=status.HTTP_200_OK)
    else:
        return error("privateTokenError")


@api_view(['POST'])
@limiter([SignUpLimiter])
def verifyEmailCodeBased(request):
    """
    verifies email using the code sent in email

    potential errors:
        requiredParams
        NoUserForEmail
        VerifiedBefore
        privateCodeError
    """
    try:
        private_code = int(request.data["code"])
        email = request.data["email"]
    except Exception:
        return error("requiredParams")
    else:
        try:
            userProfile = UserProfile.objects.get(email=email)
        except Exception:
            return error("NoUserForEmail")

        if userProfile.verified_email:
            return error("VerifiedBefore")

        if userProfile.verify_email_code == private_code:
            userProfile.verified_email = True
            userProfile.save()
            return Response({"message": "email verification was successful, you can login now!",
                             "success": "1"},
                            status=status.HTTP_200_OK)
        else:
            return error("privateCodeError")


@api_view(['POST'])
@limiter([ForgotPasswordLimiter])
def forgotPassword(request):
    """
    sends email user to reset his/her password

    potential errors:
        requiredParams
        invalidEmailError
        noSuchUser
        notVerifiedEmailError
    """
    try:
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    simple_email_set = simplify_email(email)

    if not simple_email_set['success']:
        return error("invalidEmailError")

    to_email = simple_email_set['email']

    # Check if email verified:
    userProfile = UserProfile.objects.filter(email=to_email)

    if not len(userProfile):
        return error("noSuchUser")
    else:
        userProfile = UserProfile.objects.get(email=to_email)

    if not userProfile.verified_email:
        return error("notVerifiedEmailError")

    token = token_hex(128)
    code = randint(10000000, 99999999)
    userProfile.reset_pass_token = token
    userProfile.reset_pass_code = code
    userProfile.save()

    html_content = get_template('ResetPass.html').render(context={
        'HOST': HOST,
        'PORT': PORT,
        'EMAIL_TOKEN_API': EMAIL_TOKEN_API,
        'email': to_email,
        'name': userProfile.user.username,
        'private_code': code,
        'private_token': token
    })

    send_email(subject='charity reset password',
               message='message',
               to_list=[to_email],
               html_content=html_content
               )

    return Response({"message": "email sent",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ResetPasswordLimiter])
def resetPasswordTokenBased(request):
    """
    resets password using the form sent to user

    potential errors:
        requiredParams
        differentPasswords
        privateTokenError
    """
    try:
        pass1 = request.data["pass1"]
        pass2 = request.data["pass2"]
        token = request.data["token"]
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    if pass1 != pass2:
        return error("differentPasswords")

    # Find user:
    userProfile = UserProfile.objects.get(email=email)
    user = User.objects.get(user=userProfile)

    # Check token:
    if not userProfile.reset_pass_token == token:
        return error("privateTokenError")
    else:
        # Change private token and password
        userProfile.reset_pass_token = token_hex(64)
        userProfile.save()
        user.set_password(pass1)
        user.save()

    return Response({"message": "password changed",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ResetPasswordLimiter])
def resetPasswordCodeBased(request):
    """
    resets password using the code sent to user in email

    potential errors:
        requiredParams
        differentPasswords
        privateCodeError
    """
    try:
        pass1 = request.data["pass1"]
        pass2 = request.data["pass2"]
        code = int(request.data["code"])
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    if pass1 != pass2:
        return error("differentPasswords")

    # Find user:
    userProfile = UserProfile.objects.get(email=email)
    user = User.objects.get(user=userProfile)

    # Check code:
    if not userProfile.reset_pass_code == code:
        return error("privateCodeError")
    else:
        # Change private code and password
        userProfile.reset_pass_code = randint(10000000, 99999999)
        userProfile.save()
        user.set_password(pass1)
        user.save()

    return Response({"message": "password changed",
                     "success": "1"},
                    status=status.HTTP_200_OK)


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

    return requested_user_lister(needy_list, donator_list)


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
                                                          + str(
                ["superAdmin" if userProfile.user_type == 1 else "admin"][0])})
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
