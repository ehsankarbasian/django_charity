from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status

from django.contrib.auth.models import User
from App1.models import UserProfile

from django.contrib.auth import authenticate
from django.contrib.auth import login as save_logged_in
from django.contrib.auth import logout as logout_user

from re import search as validateRegex


# Statics:
EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def error (message):
    return Response ({"status": message,
                      "success": "0"},
                    status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def login (request):
    try:
        username = request.data["username"]
        password = request.data["password"]
    except:
        return error ("requiredParams")
    else:
        user = authenticate (
                username = username,
                password = password
                )
        if user is None:
            return error ("wrongUsernameOrPass")
        else:
            save_logged_in (request, user)
            user = User.objects.get (username = username)
            return Response ({"username": user.username,
                              "email": user.email,
                              "success": "1"},
                             status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def signup (request):
    try:
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
    except:
        return error ("requiredParams")
    else:
        try:
            # Handle email tags and dot thrick:
            email_tags_string = "+".join(email.split("@")[0].split("+")[1:])
            email = "".join(
                            email.split("@")[0]
                            .split("+")[0].split(".")
                        ) + "@" + email.split("@")[1]
        except:
            return error ("invalidEmailError")
        #Validate email using regex:
        if not validateRegex(EMAIL_REGEX, email):
            return error ("invalidEmailError")
        #Handle ununique username or emails:
        elif (len(User.objects.filter(username = username))
        and len(User.objects.filter (email = email))):
            #Ununique username and email:
            return error ("emailUsernameError")
        elif len(User.objects.filter (username = username)):
            #Ununique username:
            return error ("usernameError")
        elif len(User.objects.filter (email = email)):
            #Ununique  email:
            return error ("emailError")
        else:
            user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                    )
            UserProfile.objects.create(
                    user = user,
                    email = email,
                    email_tags = email_tags_string
                    )
            save_logged_in (request, user)
            return Response ({"username": username,
                              "email": email,
                              "success": "1"},
                            status = status.HTTP_200_OK)
        
            
@api_view(['GET', 'POST'])
def logout (request):
    try:
        logout_user (request)
        return Response ({"success": "1"},
                         status = status.HTTP_200_OK)
    except:
        return error ("")
        
        
@api_view(['GET', 'POST'])
def LoadUserProfile (request):
    try:
        if not request.user_is_authenticated:
            return Response ({"error": "notLoggedIn",
                              "success": "0"},
                             status = status.HTTP_200_OK)
        username = request.data("username")
        current_user = request.user
        if username != current_user.username:
            return Response ({"error": "current_user in backend is "
                              + "different with current_user logged "
                              + "in in fronrend !!!",
                              "success": "0"},
                             status = status.HTTP_200_OK)
    except:
        return Response ({"error": "requiredParams",
                          "success": "0"},
                        status = status.HTTP_200_OK)
    else:
        #Send current_user.details to front:
        return Response ({"username": username,
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
                          "success": "1"
                          },
                        status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def SubmitUserProfile (request):
    try:
        #required fields:
        username = request.data("username")
        user_type = request.data("user_type")
        first_name = request.data("first_name")
        last_name = request.data("last_name")
        melli_code = request.data("melli_code")
        email = request.data("email")
        mobile_number = request.data("mobile_number")
        gender = request.data("gender")
    except:
        return Response ({"error": "requiredParams",
                          "success": "0"},
                         status = status.HTTP_200_OK)
    else:
        try:
            #NOT reqiured fields:
            
            #TODO: handle exiting from try ond going to
            #except wiyhout going to the else block
            job = request.data("job")
            address = request.data("address")
            house_phone = request.data("house_phone")
            workplace_phone = request.data("workplace_phone")
            married = request.data("married")
            birth_date = request.data("birth_date")
        except:
            return Response ({"error": "unriquiredParams"},
                            status = status.HTTP_200_OK)
        else:
            #create UserProfile if not exists
            #If it exists, so edit it!
            user = User.objects.get(username = username)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            userProfile = UserProfile.objects.get(user = user)
            if userProfile is None:
                UserProfile.objects.create(
                        user = user,
                        user_type = user_type,
                        first_name = first_name,
                        last_name = last_name,
                        melli_code = melli_code,
                        email = email,
                        mobile_number = mobile_number,
                        dender = gender,
                        job = job,
                        address = address,
                        house_phone = house_phone,
                        workplace_phone = workplace_phone,
                        married = married,
                        birth_date = birth_date
                        ).save()
            else:
                userProfile.update(
                        user_type = user_type,
                        first_name = first_name,
                        last_name = last_name,
                        melli_code = melli_code,
                        email = email,
                        mobile_number = mobile_number,
                        dender = gender,
                        job = job,
                        address = address,
                        house_phone = house_phone,
                        workplace_phone = workplace_phone,
                        married = married,
                        birth_date = birth_date
                        )
            return Response ({"username": username,
                             "user_type": user_type,
                             "success": "1"},
                             status = status.HTTP_200_OK)
            