"""
APIs of donatesIn are here

contains:
    generalDonate
    pendingDonates
    delivery
"""


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from App1.models import *

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *
from App1.Components.lister_functions import *


@api_view(['POST'])
def generalDonate(request):
    """
    donates money or product for not an event

    potential errors:
        requiredParams
        howToDelivery
        productQuantity
        productNotFound
        donateTypeError
        userNotFound
        userIsNeedy
        userIsNotVerified
        completeProfileFirstPlease
    """

    try:
        known = int(request.data["known"])
        TOKEN_ID = get_data_or_none(request, "TOKEN_ID")
        money_amount = get_data_or_none(request, "money_amount")
        product_id = get_data_or_none(request, "product_id")
        quantity = get_data_or_none(request, "quantity")
    except Exception:
        return error("requiredParams")

    if (product_id is not None) and (known == 0):
        return error("howToDelivery")

    userProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if TOKEN_ID is None:
        userProfile = None
    elif not len(userProfile):
        return error("userNotFound")
    else:
        userProfile = UserProfile.objects.get(token=TOKEN_ID)
        if (userProfile.melli_code == "") and (product_id is not None):
            return error("completeProfileFirstPlease")
        elif userProfile.user_type == 4:
            return error("userIsNeedy")
        elif not userProfile.verified:
            return error("userIsNotVerified")

    if known == 0:
        userProfile = None

    # Detect donate type (money/product) and then create donate:
    if (product_id is not None) and (money_amount is not None):
        return error("donateTypeError",
                     {"message": "product_id & money_amount can't be passed both"})
    elif product_id is not None:
        product_id = int(product_id)
        if quantity is None:
            return error("productQuantity")
        else:
            quantity = int(quantity)
        product = Product.objects.filter(id=product_id)
        if not len(product):
            return error("productNotFound")
        product = Product.objects.get(id=product_id)
        # Donate product:
        DonatesIn.objects.create(donator=userProfile,
                                 product=product,
                                 quantity=quantity)
    else:
        if money_amount is None:
            return error("requiredParams",
                         {"message": "money_amount & product_id can't be null both"})
        money_amount = int(money_amount)
        transaction = Transactions.objects.create(amount=money_amount,
                                                  donatorOrNeedy=userProfile,
                                                  is_in=True)
        DonatesIn.objects.create(donator=userProfile,
                                 transaction=transaction)

    return Response({"message": "donate recorded successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def pendingDonates(request):
    """
    returns all pending donates list or pending donates according to donator melli_code
     to delivery to admin or superAdmin

    potential error:
        donatorNotFound
    """
    melli_code = get_data_or_none(request, "melli_code")

    pending_query = Q(transferee=None)
    donate_set = DonatesIn.objects.filter(pending_query).order_by('-create_date')

    if melli_code is not None:
        donator = UserProfile.objects.filter(melli_code=melli_code)
        if not len(donator):
            return error("donatorNotFound")
        donator = UserProfile.objects.get(melli_code=melli_code)
        donator_query = Q(donator=donator)
        donate_set = donate_set.filter(donator_query)

    product_query = ~Q(product=None)
    donate_set = donate_set.filter(product_query)

    return donateIn_lister(donate_set)


@api_view(['POST'])
def delivery(request):
    """
    records delivery product by admin for a donate

    potential errors:
        requiredParams
        userNotFound
        userIsNotAdmin
        donateNotFound
        deliveredBefore
    """
    try:
        donate_id = int(request.data["donate_id"])
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    transferee = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(transferee):
        return error("userNotFound")
    transferee = UserProfile.objects.get(token=TOKEN_ID)
    if transferee.user_type not in [1, 2]:
        return error("userIsNotAdmin")

    donate = DonatesIn.objects.filter(id=donate_id)
    if not len(donate):
        return error("donateNotFound")
    donate = DonatesIn.objects.get(id=donate_id)
    if donate.transferee is not None:
        return error("deliveredBefore")

    product = donate.product
    product.quantity += donate.quantity
    product.save()

    donate.transferee = transferee
    donate.save()

    return Response({"message": "delivered successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)
