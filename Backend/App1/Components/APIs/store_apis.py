"""
APIs for add, edit and show products and categories will be here

contains:
    create_category
    create_subcategory
    create_product

    category_list
    subcategory_list
    product_list

    edit_category
    edit_subcategory
    edit_product

    delete_category
    delete_subcategory
    delete_product
"""


from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import json

from App1.Components.helper_functions import *
from App1.Components.lister_functions import *
from App1.Components.custom_limiter import *

from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Category, SubCategory, Product


@api_view(['POST'])
def create_category(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "create_category",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def create_subcategory(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "create_subcategory",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def create_product(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "create_product",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def category_list(request):
    """
    It returns categories as a JSON
    it has 2 modes: search or all:
        search: return categories which title contains 'search_key'
        all: returns all of categories
    """

    search_key = get_data_or_none(request, "search_key")
    search_key = ["" if not search_key else search_key][0]

    search_query = Q(title__contains=search_key)
    result_set = Category.objects.filter(search_query)

    return category_lister(result_set)


@api_view(['POST'])
def subcategory_list(request):
    """
    It returns subcategories as a JSON
    it has 4 modes: (search), (category-based), (search & category-based) and (all):
        search: return subcategories which title contains 'search_key'
        category-based: takes the 'id' of category and returns it's subcategories
        search & subcategory-based: selects according to tho both of 'search_key' and 'category_id'
        all: returns all of subcategories
    """

    search_key = get_data_or_none(request, "search_key")
    search_key = ["" if not search_key else search_key][0]

    category_id = get_data_or_none(request, "category_id")

    search_query = Q(title__contains=search_key)
    category_query = Q(category__id=category_id)

    result_set = SubCategory.objects.filter(search_query)
    if category_id:
        result_set = result_set.filter(category_query)

    return subcategory_lister(result_set)


@api_view(['POST'])
def product_list(request):
    """
    It returns products as a JSON
    it has 6 modes: (search), (category-based), (subcategory-based),
                    (search & category-based), (search & subcategory-based) and (all):
        search: return products which title contains 'search_key'
        category-based: takes the 'id' of category and returns it's products
        subcategory-based: takes the 'id' of subcategory and returns it's products

        search & category-based: selects according to tho both of 'search_key' and 'category_id'
        search & subcategory-based: selects according to tho both of 'search_key' and 'subcategory_id'

        all: returns all of products
    """

    search_key = get_data_or_none(request, "search_key")
    search_key = ["" if not search_key else search_key][0]

    category_id = get_data_or_none(request, "category_id")
    subcategory_id = get_data_or_none(request, "subcategory_id")

    search_query = Q(title__contains=search_key)
    category_query = Q(subCategory__category__id=category_id)
    subcategory_query = Q(subCategory__id=subcategory_id)

    result_set = Product.objects.filter(search_query)
    if category_id:
        result_set = result_set.filter(category_query)
    if subcategory_id:
        result_set = result_set.filter(subcategory_query)

    return product_lister(result_set)


@api_view(['POST'])
def edit_category(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "edit_category",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_subcategory(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "edit_subcategory",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_product(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "edit_product",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_category(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "delete_category",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_subcategory(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "delete_subcategory",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_product(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "delete_product",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)
