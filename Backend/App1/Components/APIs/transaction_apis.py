"""
APIs of transactions are here

contains:
    transactionList
    resentTransactionList
    biggestTransactionList
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
def transactionList(request):
    """
    lists all or filtered money transactions

    potential errors:
        requiredParams
        userNotFound
        filteredUserNotFound
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
                return error("filteredUserNotFound")
        else:
            user_filter = UserProfile.objects.all()

    user_query = Q(donatorOrNeedy__in=user_filter)
    result_set = Transactions.objects.filter(user_query).order_by('-create_date_time')

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
def recentTransactionList(request):
    """
    lists the most recent transactions

    potential error:
        countIsNotInt
    """
    try:
        count = get_data_or_none(request, "count")
        count = [int(count) if count is not None else 10][0]
    except Exception:
        return error("countIsNotInt")

    result_set = Transactions.objects.all().order_by('-create_date_time')[:count]
    return transaction_lister(result_set)


@api_view(['POST'])
def biggestTransactionList(request):
    """
    lists the most big-amount transactions

    potential error:
        countIsNotInt
    """
    try:
        count = get_data_or_none(request, "count")
        count = [int(count) if count is not None else 10][0]
    except Exception:
        return error("countIsNotInt")

    result_set = Transactions.objects.all().order_by('-amount')[:count]
    return transaction_lister(result_set)
