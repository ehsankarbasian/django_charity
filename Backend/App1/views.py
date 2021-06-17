from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from App1.models import Image
from App1.models import UserProfile
from App1.models import Event
from App1.models import Transactions
from App1.models import DonatesIn
from App1.models import Product
from App1.models import NeedRequest
from App1.models import Category
from App1.models import SubCategory

from Backend.settings import HOST, PORT

from App1.serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *
from App1.Components.APIs.store_apis import *
from App1.Components.APIs.transaction_apis import *
from App1.Components.APIs.donate_apis import *
from App1.Components.APIs.need_request_apis import *
from App1.Components.APIs.admin_management_apis import *


# API functions:
@api_view(['POST'])
def email(request):
    """ potential error: requiredParams """
    try:
        subject = request.data["subject"]
        message = request.data["message"]
        to_list = request.data["to_list"]
        separated_with = request.data["separated_with"]
        if len(separated_with) == 0:
            separated_with = " "
    except Exception:
        return error("requiredParams")

    to_list = to_list.split(separated_with)
    send_text_email(subject, message, to_list)

    return Response({"message": "email sent",
                     "success": "1"},
                    status=status.HTTP_200_OK)


class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response({"image_url": image_serializer.data["image"]},
                            status=status.HTTP_200_OK)
        else:
            print('IMAGE SERIALIZER ERROR', image_serializer.errors)
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
