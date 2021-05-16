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

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *
from App1.Components.APIs.store_apis import *


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
def generalDonate(request):
    """
        donates money or product for not an event

        potential errors:
            requiredParams
            productQuantity
            productNotFound
            donateTypeError
            userNotFound
            userIsNeedy
            userIsNotVerified
        """

    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        money_amount = get_data_or_none(request, "money_amount")
        product_id = get_data_or_none(request, "product_id")
    except Exception:
        return error("requiredParams", {"message": "user TOKEN_API is not passed"})

    # Find and check user:
    user = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(user):
        return error("userNotFound")
    else:
        user = UserProfile.objects.get(token=TOKEN_ID)
        if user.user_type == 4:
            return error("userIsNeedy")
        if not user.verified:
            return error("userIsNotVerified")

    # Detect donate type (money/product) and then create donate:
    if product_id:
        if money_amount:
            return error("donateTypeError", {"message": "product_id & money_amount can't be passed both"})
        try:
            product_id = int(product_id)
            quantity = int(request.data["quantity"])
            product = Product.objects.filter(id=product_id)
            if not len(product):
                return error("productNotFound")
            else:
                product = Product.objects.get(id=product_id)
            # Donate product:
            DonatesIn.objects.create(donator=user,
                                     product=product,
                                     quantity=quantity)
            product.quantity += quantity
            product.save()
        except Exception:
            return error("productQuantity")
    else:
        if not money_amount:
            return error("requiredParams", {"message": "money_amount & product_id can't be null both"})
        else:
            money_amount = int(money_amount)
            transaction = Transactions.objects.create(amount=money_amount,
                                                      donatorOrNeedy=user,
                                                      is_in=True)
            DonatesIn.objects.create(donator=user,
                                     transaction=transaction)

    return Response({"message": "donate recorded successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)
