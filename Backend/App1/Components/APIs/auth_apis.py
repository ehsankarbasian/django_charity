"""
APIs of auth and reset-pass, will be here

contains APIs:
    login
    signup
    logout

    verifyEmailTokenBased
    verifyEmailCodeBased

    forgotPassword
    resetPasswordTokenBased
    resetPasswordCodeBased

    notVerifiedUserSet
    verifiedDonatorSet
    adminSet
    verifyOrRejectUser
"""

from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.template.loader import get_template
from django.http import HttpResponse

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *
from re import search as validateRegex
from django.db.models import Q
from random import randint

from Backend.settings import HOST, PORT, FRONT_PORT

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import ExpiredTokens

from Backend.urls import TOKEN_API, EMAIL_TOKEN_API, HOST, PORT

EMAIL_REGEX = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


@api_view(['POST'])
@limiter([LoginLimiter])
def login(request):
    """ potential errors: requiredParams, wrongUsernameOrPass, emailVerificationError """
    try:
        username = request.data["username"]
        password = request.data["password"]
    except Exception:
        return error("requiredParams")
    else:
        user = authenticate(username=username,
                            password=password)
        if user is None:
            return error("wrongUsernameOrPass")

        user = User.objects.get(username=username)
        userProfile = UserProfile.objects.get(user=user)

        if not userProfile.verified_email:
            return error("emailVerificationError")

        request.session['user_id'] = user.id
        return Response({"username": user.username,
                         "email": userProfile.email,
                         "token": userProfile.token,
                         "user_type": userProfile.user_type,
                         "image_url": userProfile.profile_image_url,
                         "success": "1"},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SignUpLimiter])
def signup(request):
    """
    user signup according to user_type
    just to signup as donator or needy
    emails to user to verify it

    potential errors: requiredParams, invalidEmailError, emailUsernameError
        usernameError, emailError, notAllowedUserTypeError
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

        if not validateRegex(EMAIL_REGEX, simple_email):
            return error("invalidEmailError")

        # Handle before-used username or emails or Both:
        username_error = len(User.objects.filter(username=username))
        email_error = bool(len(User.objects.filter(email=original_email))
                           or len(User.objects.filter(email=simple_email)))
        if username_error and email_error:
            return error("emailUsernameError")
        elif username_error:
            return error("usernameError")
        elif email_error:
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
                password=password)
            UserProfile.objects.create(
                user=user,
                email=simple_email,
                token=token,
                email_tags=email_tags_string,
                user_type=user_type,
                verify_email_code=verify_email_code,
                verify_email_token=verify_email_token)

            # Sending html based email to user to verify his/her email:
            html_content = get_template('EmailVerification.html').render(context={
                'HOST': HOST,
                'PORT': PORT,
                'EMAIL_TOKEN_API': EMAIL_TOKEN_API,
                'email': simple_email,
                'name': username,
                'private_code': verify_email_code,
                'private_token': verify_email_token})
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
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_ID)):
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
    """ potential errors: requiredParams, privateTokenError """
    result = "Your email verified successfully"
    try:
        private_token = request.data["token"]
        email = request.data["email"]
        userProfile = UserProfile.objects.get(email=email)
        if userProfile.verified_email:
            result = "ERROR: your email verified before"
        elif userProfile.verify_email_token == private_token:
            userProfile.verified_email = True
            userProfile.save()
        else:
            result = "ERROR: privateTokenError"
    except Exception:
        result = "ERROR: requiredParams"

    template = get_template('EmailDestination.html').render(context={
        'HOST': HOST,
        'PORT': FRONT_PORT,
        'result': result,
        'message': "you've submitted email verification using link"})

    return HttpResponse(template)


@api_view(['POST'])
@limiter([SignUpLimiter])
def verifyEmailCodeBased(request):
    """ potential errors: requiredParams, NoUserForEmail, VerifiedBefore, privateCodeError """
    try:
        private_code = int(request.data["code"])
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(email=email)):
        return error("NoUserForEmail")
    userProfile = UserProfile.objects.get(email=email)

    if userProfile.verified_email:
        return error("VerifiedBefore")

    if userProfile.verify_email_code != private_code:
        return error("privateCodeError")

    userProfile.verified_email = True
    userProfile.save()
    return Response({"message": "email verification was successful, you can login now!",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ForgotPasswordLimiter])
def forgotPassword(request):
    """
    sends email to user to reset his/her password

    potential errors: requiredParams, invalidEmailError, noSuchUser, notVerifiedEmailError
    """
    try:
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    simple_email_set = simplify_email(email)

    if not simple_email_set['success']:
        return error("invalidEmailError")

    to_email = simple_email_set['email']

    if not len(UserProfile.objects.filter(email=to_email)):
        return error("noSuchUser")
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
        'private_token': token})
    send_email(subject='charity reset password',
               message='message',
               to_list=[to_email],
               html_content=html_content)

    return Response({"message": "email sent",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ResetPasswordLimiter])
def resetPasswordTokenBased(request):
    """ potential errors: requiredParams, differentPasswords, privateTokenError """
    result = "Your email verified successfully"
    try:
        pass1 = request.data["pass1"]
        pass2 = request.data["pass2"]
        token = request.data["token"]
        email = request.data["email"]

        if pass1 != pass2:
            result = "ERROR: differentPasswords"
        userProfile = UserProfile.objects.get(email=email)
        user = User.objects.get(user=userProfile)

        if userProfile.reset_pass_token != token:
            result = "ERROR: privateTokenError"
        else:
            userProfile.reset_pass_token = token_hex(64)
            userProfile.save()
            user.set_password(pass1)
            user.save()

    except Exception:
        result = "ERROR: requiredParams"

    template = get_template('EmailDestination.html').render(context={
        'HOST': HOST,
        'PORT': FRONT_PORT,
        'result': result,
        'message': "you've submitted change password request using link"})

    return HttpResponse(template)


@api_view(['POST'])
@limiter([ResetPasswordLimiter])
def resetPasswordCodeBased(request):
    """ potential errors: requiredParams, differentPasswords, userNotFound, privateCodeError """
    try:
        pass1 = request.data["pass1"]
        pass2 = request.data["pass2"]
        code = int(request.data["code"])
        email = request.data["email"]
    except Exception:
        return error("requiredParams")

    if pass1 != pass2:
        return error("differentPasswords")

    if not len(UserProfile.objects.filter(email=email)):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(email=email)
    user = User.objects.get(user=userProfile)

    if not userProfile.reset_pass_code == code:
        return error("privateCodeError")

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
    returns the list of not verified donators and needies to verify by superAdmin
    potential errors: requiredParams, adminNotFound, notAdminOrSuperAdmin
    """
    try:
        TOKEN_API = request.data["TOKEN_API"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_API)):
        return error("adminNotFound")
    adminProfile = UserProfile.objects.get(token=TOKEN_API)

    if adminProfile.user_type not in [1, 2]:
        return error("notAdminOrSuperAdmin")

    donator_list = UserProfile.objects.filter(verified=False).filter(user_type=3)
    needy_list = UserProfile.objects.filter(verified=False).filter(user_type=4)

    return requested_user_lister(needy_list, donator_list)


@api_view(['POST'])
def verifiedDonatorSet(request):
    """
    the list of verified donators (verified by admin and verified email)
    potential errors: requiredParams, adminNotFound, notSuperAdminOrAdmin
    """
    try:
        TOKEN_API = request.data["TOKEN_API"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_API)):
        return error("adminNotFound")
    adminProfile = UserProfile.objects.get(token=TOKEN_API)

    if adminProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    donator_query = Q(user_type=3) & Q(verified=True) & Q(verified_email=True)
    donator_list = UserProfile.objects.filter(donator_query)

    return Response(user_lister(donator_list),
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def adminSet(request):
    """ potential errors: requiredParams, adminNotFound, notSuperAdminOrAdmin """
    try:
        TOKEN_API = request.data["TOKEN_API"]
    except Exception:
        return error("requiredParams")

    if not len(UserProfile.objects.filter(token=TOKEN_API)):
        return error("adminNotFound")
    adminProfile = UserProfile.objects.get(token=TOKEN_API)

    if adminProfile.user_type not in [1, 2]:
        return error("notSuperAdminOrAdmin")

    admin_query = Q(user_type=2)
    admin_list = UserProfile.objects.filter(admin_query)

    return Response(user_lister(admin_list),
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([VerifyOrRejectUserLimiter])
def verifyOrRejectUser(request):
    """
    potential errors: requiredParams, notSuperAdmin
        adminNotFound, verifiedBefore, userTypeError, userNotFound
    """
    try:
        TOKEN_API = request.data["TOKEN_API"]
        user_id = int(request.data["user_id"])
        accept = int(request.data["action"])
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

    if accept:
        userProfile.verified = True
        userProfile.save()
    else:
        userProfile.user.delete()
        userProfile.delete()

    return Response({"message": "user " + str(["verified" if accept else "rejected (deleted)"][0]) + " successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)
