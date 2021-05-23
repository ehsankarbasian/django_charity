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
        completeProfileFirstPlease
    """

    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        money_amount = get_data_or_none(request, "money_amount")
        product_id = get_data_or_none(request, "product_id")
    except Exception:
        return error("requiredParams", {"message": "user TOKEN_API is not passed"})

    try:
        userProfile = UserProfile.objects.get(token=TOKEN_ID)
        if (userProfile.user_type == 1) or (userProfile.user_type == 2):
            return error("userTypeError", {"explanation": "user_type is "
                                           + str(["superAdmin" if userProfile.user_type == 1 else "admin"][0])})
        elif not len(userProfile.melli_code):
            return error("completeProfileFirstPlease")
    except Exception:
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


@api_view(['POST'])
def pending_donates(request):
    """
    returns all pending donates list or pending donates according to donator melli_code
     to delivery to admin or superAdmin

    potential error:
        donatorNotFound
    """
    pending_query = Q(transferee=None)
    donate_set = DonatesIn.objects.filter(pending_query).order_by('-create_date')

    melli_code = get_data_or_none(request, "melli_code")
    if melli_code is not None:
        donator = UserProfile.objects.filter(melli_code=melli_code)
        if not len(donator):
            return error("donatorNotFound")
        donator = UserProfile.objects.get(melli_code=melli_code)
        result_set = []
        for donate in donate_set:
            if donate.donator == donator:
                result_set.append(donate)
    else:
        result_set = donate_set

    return donateIn_lister(result_set)


@api_view(['POST'])
def delivery(request):
    """
    records delivery product by admin for a donate

    potential errors:
        requiredParams
        userNotFound
        userNotAdmin
        donateNotFound
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
        return error("userNotAdmin")

    donate = DonatesIn.objects.filter(id=donate_id)
    if not len(donate):
        return error("donateNotFound")
    donate = DonatesIn.objects.get(id=donate_id)

    donate.transferee = transferee
    donate.save()

    return Response({"message": "delivered successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def transactionList(request):
    """
    lists all or filtered money transactions

    potential errors:
        requiredParams
        userNotFound
        filterUserNotFound
    """
    SORT_BY = ["", "amount", "create_date"]

    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        is_in = get_data_or_none(request, "is_in")
        sort_by = get_data_or_none(request, "sort_by")
        sort_type = get_data_or_none(request, "sort_type")
        amount_max = get_data_or_none(request, "amount_max")
        amount_min = get_data_or_none(request, "amount_min")
        filter_by_user = get_data_or_none(request, "filter_by_user")
    except Exception:
        return error("requiredParams")

    user = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(user):
        return error("userNotFound")
    user = UserProfile.objects.get(token=TOKEN_ID)

    if user.user_type in [3, 4]:
        user_filter = UserProfile.objects.filter(token=TOKEN_ID)
    else:
        if filter_by_user:
            user_filter = UserProfile.objects.filter(melli_code=filter_by_user)
            if not len(user_filter):
                return error("filterUserNotFound")
        else:
            user_filter = UserProfile.objects.all()

    user_query = Q(donatorOrNeedy__in=user_filter)
    result_set = Transactions.objects.filter(user_query).order_by('-create_date')

    if is_in is not None:
        is_in = bool(is_in)
        result_set = result_set.filter(is_in=is_in)

    if amount_max:
        amount_max = int(amount_max)
        max_query = Q(amount__lte=amount_max)
        result_set = result_set.filter(max_query)

    if amount_min:
        amount_min = int(amount_min)
        min_query = Q(amount__gte=amount_min)
        result_set = result_set.filter(min_query)

    sort_type = ["" if sort_type == "+" else "-"][0]

    if sort_by is not None:
        sort_by = int(sort_by)
        result_set = result_set.order_by(sort_type + SORT_BY[sort_by])

    return transaction_lister(result_set)


@api_view(['POST'])
def resentTransactionList(request):
    """
    lists the most recent transactions

    potential errors:
        requiredParams
    """
    try:
        count = get_data_or_none(request, "count")
    except Exception:
        return error("requiredParams")

    count = [int(count) if count else 10][0]

    result_set = Transactions.objects.all().order_by('-create_date')[:count]

    return transaction_lister(result_set)


@api_view(['POST'])
def createNeedRequest(request):
    """
    creates NeedRequest

    potential errors:
        requireParams
        userNotFound
        userTypeError
        productNotFound
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
        title = request.data["title"]
        description = request.data["description"]
        product_id = int(request.data["product_id"])
    except Exception:
        return error("requiredParams")

    # Find user:
    userProfile = UserProfile.objects.filter(token=TOKEN_ID)
    if not len(userProfile):
        return error("userNotFound")
    userProfile = UserProfile.objects.get(token=TOKEN_ID)

    if userProfile.user_type != 4:
        return error("userTypeError", {"message": "you are not needy"})
    elif not userProfile.verified:
        return error("notVerifiedNeedy")

    # Find product:
    try:
        product = Product.objects.get(id=product_id)
    except Exception:
        return error("productNotFound")

    # Create NeedRequest:
    NeedRequest.objects.create(creator=userProfile,
                               status=1,  # TODO: delete this line after verify NeedRequest by admin
                               title=title,
                               description=description,
                               product=product)

    return Response({"message": "NeedRequest created successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def requestedNeedRequestList(request):
    """
    list of NeedRequest with status 0

    potential errors:
        requiredParams
        userNotFound
        userNotSuperAdmin
    """
    try:
        TOKEN_ID = request.data["TOKEN_ID"]
    except Exception:
        return error("requiredParams")

    # Find user:
    try:
        userProfile = UserProfile.objects.get(token=TOKEN_ID)
    except Exception:
        return error("userNotFound")

    # Check whether superAdmin/admin or not:
    if userProfile.user_type not in [1, 2]:
        return error("userNotSuperAdmin")

    # Find NeedRequests with status 0:
    needRequest_set = list(NeedRequest.objects.filter(status=0))

    return needRequest_lister(needRequest_set)


@api_view(['POST'])
def editNeedrequestByAdmin(request):
    try:
        token = request.data["TOKEN_ID"]
        NeedRequest_id = request.data["NeedRequest_id"]

        title = request.data["title"]
        description = request.data["description"]
        product_id = request.data["product_TOKEN_ID"]
        feedback = request.data["feedback"]
    except Exception:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("Wrong TOKEN_ID")
        # Find Product
        try:
            product = Product.objects.get(token=product_id)
        except Exception:
            return error("Wrong Product_TOKEN_ID")

        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Edit NeedRequest:
        try:
            needRequest = NeedRequest.objects.get(id=NeedRequest_id)
        except Exception:
            return error("WrongNeedrequestId")
        else:

            needRequest.title = title
            needRequest.description = description
            needRequest.product = product
            needRequest.edited = True
            needRequest.edited_by = userProfile.id
            needRequest.feedback = feedback
            needRequest.status = 1
            needRequest.enabled = True
            needRequest.save()

        return Response({"message": "NeedRequest edited",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def disableNeedrequest(request):
    try:
        token = request.data["TOKEN_ID"]
        needrequest_id = request.data["NeedRequest_id"]
    except Exception:
        return error("requiredParams")
    else:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("Wrong TOKEN_ID")

        # Check whether SuperAdmin or not:
        if userProfile.user_type != 1:
            return error("NotSuperAdmin")

        # Disable the event:
        needRequest = NeedRequest.objects.get(id=needrequest_id)
        needRequest.enabled = False
        needRequest.save()

        return Response({"message": "NeedRequest disabled",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def userNeedrequest(request):
    try:
        token = request.data["token"]
    except Exception:
        return error("requiredParams")

    try:
        userProfile = UserProfile.objects.get(token=token)
        user = userProfile.user
        needrequestSet = NeedRequest.objects.filter(creator=user)
        return create_needrequest_set(needrequestSet)
    except Exception:
        return error("noSuchUser")


@api_view(['POST'])
def deleteNeedrequest(request):
    try:
        needrequest_id = request.data["NeedRequest_id"]
        token = request.data["token"]
    except Exception:
        return error("requiredParams")

    try:
        needRequest = NeedRequest.objects.get(id=needrequest_id)
    except Exception:
        return error("noSuchNeedrequest")

    try:
        userProfile = UserProfile.objects.get(token=token)
        user = userProfile.user
    except Exception:
        return error("noSuchUser")

    if needRequest.creator.username != user.username:
        return error("youAreNotCreator")

    if needRequest.status != 1:
        needRequest.delete()
    else:
        return error("acceptedNeedrequest")

    return Response({"success": "1",
                     "message": "The NeedRequest deleted successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def editNeedrequestByUser(request):
    try:
        token = request.data["TOKEN_ID"]
        needrequest_id = request.data["NeedRequest_id"]

        title = request.data["title"]
        description = request.data["description"]
        product_id = request.data["product_TOKEN_ID"]
    except Exception:
        return error("requiredParams")
    else:
        # Find user:
        try:
            userProfile = UserProfile.objects.get(token=token)
        except Exception:
            return error("noSuchUser")

        # Find product:
        try:
            product = Product.objects.get(token=product_id)
        except Exception:
            return error("noSuchProduct")

        try:
            needRequest = NeedRequest.objects.get(id=needrequest_id)
        except Exception:
            return error("noSuchNeedrequest")
        else:
            if needRequest.creator != userProfile.user:
                return error("youAreNotCreator")
            elif needRequest.status == -1:
                return error("rejectedNeedrequest")

            needRequest.title = title
            needRequest.description = description
            needRequest.product = product
            needRequest.edited = True
            needRequest.edited_by = userProfile.id
            needRequest.status = 0
            needRequest.save()

        return Response({"message": "NeedRequest edited",
                         "success": "1"
                         },
                        status=status.HTTP_200_OK)
