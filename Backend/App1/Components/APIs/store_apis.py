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


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "category_list",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def subcategory_list(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "subcategory_list",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def product_list(request):
    """


    potential errors:
        requiredParams
    """
    try:
        pass
    except Exception:
        return error("requiredParams")

    return Response({"message": "product_list",
                     "success": "1"
                     },
                    status=status.HTTP_200_OK)


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
