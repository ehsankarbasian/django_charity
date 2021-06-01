"""
APIs related to show and edit profile, will be here

contains:
    loadUserProfile
    submitUserProfile
    editProfileImage
    userBio
"""


from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *

from django.contrib.auth.models import User
from App1.models import UserProfile


@api_view(['POST'])
@limiter([ProfileLimiter])
def loadUserProfile(request):
    """
    loads user profile if logged in

    potential errors:
        requiredParams
        DoesNotExist
    """
    try:
        username = request.data["username"]
    except Exception:
        return error("requiredParams")

    try:
        user = User.objects.get(username=username)
        current_user = UserProfile.objects.get(user=user)
    except Exception:
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
                         "verified_needy": current_user.verified,
                         "verified": current_user.verified,
                         "verified_mobile": current_user.verified_mobile,
                         "verified_email": current_user.verified_email,
                         "is_profile_completed": current_user.completed,
                         "image_url": current_user.profile_image_url,
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([ProfileLimiter])
def submitUserProfile(request):
    """
    edits user profile according to new inputs by user if logged in

    potential error:
        requiredParams
        noSuchUser
    """
    try:
        # Required fields:
        username = request.data["username"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        melli_code = request.data["melli_code"]
        mobile_number = request.data["mobile_number"]
    except Exception:
        return error("requiredParams")
    else:
        # Check user:
        user = User.objects.filter(username=username)
        if not len(user):
            return error("noSuchUser")
        else:
            user = user[0]
        userProfile = UserProfile.objects.get(user=user)

        # NOT required fields:
        job = get_data_or_none(request, "job")
        address = get_data_or_none(request, "address")
        house_phone = get_data_or_none(request, "house_phone")
        workplace_phone = get_data_or_none(request, "workplace_phone")
        gender = get_data_or_none(request, "gender")
        married = get_data_or_none(request, "married")
        birth_date = get_data_or_none(request, "birth_date")
        profile_image_url = get_data_or_none(request, "image_url")

        # Update User:
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update UserProfile:
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

        if profile_image_url is not None:
            userProfile.profile_image_url = profile_image_url

        userProfile.completed = True
        userProfile.save()

        return Response({"username": username,
                         "email": userProfile.email,
                         "user_type": userProfile.user_type,
                         "success": "1"},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def editProfileImage(request):
    """
    changes profile image

    potential errors:
        requiredParams
        wrongUsernameOrPass
    """
    try:
        username = request.data["username"]
        password = request.data["password"]
        image_url = request.data["image_url"]
    except Exception:
        return error("requiredParams")

    user = authenticate(username=username,
                        password=password)
    if user is None:
        return error("wrongUsernameOrPass")

    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.profile_image_url = image_url
    user_profile.save()

    return Response({"message": "profile image changed successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([BioLimiter])
def userBio(request):
    """
    shows user bio for other users
    no need to login, just the user's username needed

    potential errors:
        requiredParams
        DoesNotExist
    """
    try:
        username = request.data["username"]
    except Exception:
        return error("requiredParams")

    try:
        user = User.objects.get(username=username)
        userProfile = UserProfile.objects.get(user=user)
    except Exception:
        return error("DoesNotExist")
    else:
        # Send current_user.bio to front:
        return Response({"username": username,
                         "user_type": userProfile.user_type,
                         "first_name": userProfile.first_name,
                         "last_name": userProfile.last_name,
                         "email": userProfile.email,
                         "image_url": userProfile.profile_image_url,
                         "verified_needy": userProfile.verified,
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)
