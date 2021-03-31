from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status

from django.contrib.auth.models import User
from App1.models import UserProfile

from django.contrib.auth import authenticate

@api_view(['GET', 'POST'])
def login (request):
    try:
        username = request.data["username"]
        password = request.data["password"]
    except:
        return Response ({"error": "Fill all fields please."},
                         status = status.HTTP_400_BAD_REQUEST)
    else:
        user = authenticate (
                username = username,
                password = password
                )
        if user is None:
            return Response ({"error": "Wrong username or password."},
                             status = status.HTTP_401_UNAUTHORIZED)
        else:
            user = User.objects.get (username = username)
            return Response ({"username": user.username,
                              "email": user.email},
                             status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def signup (request):
    try:
        username = request.data["username"]
        email = request.date["email"]
        password = request.data["password"]
    except:
        return Response ({"error": "Fill all fields please."},
                         status = status.HTTP_400_BAD_REQUEST)
    else:
        User.objects.create_user(
                username = username,
                email = email,
                password = password
                )
        return Response ({"username": username,
                          "email": email},
                         status = status.HTTP_200_OK)
        

#@api_view()
#def editProfile (request):
#    try:
#        #required main
#        pass
#    except:
#        return Response ({"error": "Complete all reqired fields please."},
#                         status = status.HTTP_400_BAD_REQUEST)
#   else:
#        #not reqiured main
#        #create UserProfile
#        return Response ({"username": username},
#                         status = status.HTTP_200_OK)