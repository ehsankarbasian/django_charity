from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event
from App1.models import Transactions
from App1.models import DonatesIn
from App1.models import Product
from App1.models import NeedRequest
from App1.models import Category
from App1.models import SubCategory

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
    """
    It's an API to send email from ntm.patronage@gmail.com to a list
    it can be used by front end too

    potential error:
        requiredParams
    """
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


@api_view(['POST'])
def dataAnalyze(request):
    category_number = len(Category.objects.all())
    subcategory_number = len(SubCategory.objects.all())
    category_product = {}
    subcategory_product = {}

    for category in Category.objects.all():
        category_product[category.title] = 0
        for subcategory in SubCategory.objects.filter(category=category):
            subcategory_product[subcategory.title] = len(Product.objects.filter(subCategory=subcategory))
            category_product[category.title] += subcategory_product[subcategory.title]

    zero = 0
    one_ten = 0
    eleven_hundred = 0
    hundred_plus = 0
    for product in Product.objects.all():
        quantity = product.quantity
        if quantity == 0:
            zero += 1
        elif 1 <= quantity <= 10:
            one_ten += 1
        elif 11 <= quantity <= 100:
            eleven_hundred += 1
        else:
            hundred_plus += 1

    return Response({"category_number": category_number,
                     "subcategory_number": subcategory_number,
                     "category_product": category_product,
                     "subcategory_product": subcategory_product,
                     "zero": zero,
                     "one_ten": one_ten,
                     "eleven_hundred": eleven_hundred,
                     "hundred_plus": hundred_plus,
                     "success": "1"},
                    status=status.HTTP_200_OK)
