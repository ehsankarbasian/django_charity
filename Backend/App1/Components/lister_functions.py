"""
The functions that adapts a queryset in JSONs to use by frontend

contains:
    user_lister
    requested_user_lister
    event_lister
    category_lister
    subcategory_lister
    product_lister
    transaction_lister
"""


from rest_framework.response import Response
from rest_framework import status
from App1.Components.item_functions import *


def user_lister(user_queryset):
    user_json = {}
    for user in user_queryset:
        user_json[user.id] = user_item(user)

    return user_json


def requested_user_lister(needy_queryset, donator_queryset, pagination_params=None):
    """
    creates json-based user set to show

    the JSON contains: "id", "username", "user_type", "first_name", "last_name",
    "melli_code", "email", "job", "address", "mobile_number", "house_phone",
    "workplace_phone", "gender", "married", "birth_date", "signup_date"

    it gets help from user_item() function
    """
    if pagination_params:
        return error("TODO", {"message": "Have no pagination yet; coming soon"})

    needy_json = user_lister(needy_queryset)
    donator_json = user_lister(donator_queryset)

    empty_needy = [0 if len(needy_json) else 1]
    empty_donator = [0 if len(donator_json) else 1]

    final_json = {"success": "1",
                  "empty_needy": empty_needy[0],
                  "empty_donator": empty_donator[0],
                  "pagination_params": pagination_params,
                  "needy_set": needy_json,
                  "donator_set": donator_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def event_lister(event_queryset, pagination_params=None):
    """
    creates an event_set according to queryset
    it's used in APIs that return several events to front
    it passes pagination params to front if exists too
    """
    # Create a json for an event:
    event_json = {}
    for event in event_queryset:
        event_json[event.id] = event_item(event)

    empty = [0 if len(event_json) else 1]
    final_json = {"success": "1",
                  "empty": empty[0],
                  "pagination_params": pagination_params,
                  "event_set": event_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def category_lister(category_queryset):
    category_json = {}
    for category in category_queryset:
        category_json[category.id] = category_item(category)

    final_json = {"success": "1",
                  "empty": [0 if len(category_json) else 1][0],
                  "count": len(category_queryset),
                  # "pagination_params": pagination_params,
                  "category_set": category_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def subcategory_lister(subcategory_queryset):
    subcategory_json = {}
    for subcategory in subcategory_queryset:
        subcategory_json[subcategory.id] = subcategory_item(subcategory)

    final_json = {"success": "1",
                  "empty": [0 if len(subcategory_json) else 1][0],
                  "count": len(subcategory_queryset),
                  # "pagination_params": pagination_params,
                  "subcategory_set": subcategory_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def product_lister(product_queryset):
    product_json = {}
    for product in product_queryset:
        product_json[product.id] = product_item(product)

    final_json = {"success": "1",
                  "empty": [0 if len(product_json) else 1][0],
                  "count": len(product_queryset),
                  # "pagination_params": pagination_params,
                  "product_set": product_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)


def transaction_lister(transaction_queryset):
    transaction_json = {}
    for transaction in transaction_queryset:
        transaction_json[transaction.id] = transaction_item(transaction)

    final_json = {"success": "1",
                  "empty": [0 if len(transaction_json) else 1][0],
                  "count": len(transaction_queryset),
                  # "pagination_params": pagination_params,
                  "transaction_set": transaction_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)
