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

    the_category
    the_subcategory
    the_product
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
    creates a new category with a title

    potential errors:
        requiredParams
        notUniqueTitle
    """
    try:
        title = request.data["title"]
    except Exception:
        return error("requiredParams")

    if len(Category.objects.filter(title=title)):
        return error("notUniqueTitle")

    category = Category.objects.create(title=title)

    return Response({"message": "category created successfully",
                     "id": category.id,
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def create_subcategory(request):
    """
    creates a new subcategory with a title in a category

    potential errors:
        requiredParams
        notUniqueTitle
        categoryNotFound
    """
    try:
        title = request.data["title"]
        category_id = request.data["category_id"]
    except Exception:
        return error("requiredParams")

    if len(SubCategory.objects.filter(title=title)):
        return error("notUniqueTitle")

    if not len(Category.objects.filter(id=category_id)):
        return error("categoryNotFound")
    category = Category.objects.get(id=category_id)
    subcategory = SubCategory.objects.create(title=title, category=category)

    return Response({"message": "subcategory created successfully",
                     "id": subcategory.id,
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def create_product(request):
    """
    creates a new product with a title in a subcategory

    potential errors:
        requiredParams
        notUniqueTitle
        subcategoryNotFound
    """
    try:
        title = request.data["title"]
        quantity = int(request.data["quantity"])
        subcategory_id = request.data["subcategory_id"]
    except Exception:
        return error("requiredParams")

    if len(Product.objects.filter(title=title)):
        return error("notUniqueTitle")

    if not len(SubCategory.objects.filter(id=subcategory_id)):
        return error("subcategoryNotFound")
    subcategory = SubCategory.objects.get(id=subcategory_id)
    product = Product.objects.create(title=title, quantity=quantity,
                                     subCategory=subcategory)

    return Response({"message": "product created successfully",
                     "id": product.id,
                     "success": "1"},
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
    edits the title of a category

    potential errors:
        requiredParams
        notUniqueTitle
        categoryNotFound
    """
    try:
        category_id = request.data["category_id"]
        title = request.data["title"]
    except Exception:
        return error("requiredParams")

    if len(Category.objects.filter(title=title)):
        return error("notUniqueTitle")

    if not len(Category.objects.filter(id=category_id)):
        return error("categoryNotFound")
    category = Category.objects.get(id=category_id)
    category.title = title
    category.save()

    return Response({"message": "category edited successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_subcategory(request):
    """
    edits the title and category of a subcategory

    potential errors:
        requiredParams
        notUniqueTitle
        subcategoryNotFound
        categoryNotFound
    """
    try:
        subcategory_id = request.data["subcategory_id"]
        title = get_data_or_none(request, "title")
        category_id = get_data_or_none(request, "category_id")
    except Exception:
        return error("requiredParams")

    if not (title or category_id):
        return error("requiredParams", {
            "message": "at least one of 'title' or 'category_id' must be passed"})

    if len(SubCategory.objects.filter(title=title)):
        return error("notUniqueTitle")

    if not len(SubCategory.objects.filter(id=subcategory_id)):
        return error("subcategoryNotFound")
    if category_id:
        if not len(Category.objects.filter(id=category_id)):
            return error("categoryNotFound")
    subcategory = SubCategory.objects.get(id=subcategory_id)
    subcategory.title = [title if title else subcategory.title][0]
    subcategory.category = [Category.objects.get(id=category_id) if category_id
                            else subcategory.category][0]
    subcategory.save()

    return Response({"message": "subcategory edited successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_product(request):
    """
    edits the title, subcategory and quantity of a product

    potential errors:
        requiredParams
        notUniqueTitle
        productNotFound
        subcategoryNotFound
    """
    try:
        product_id = int(request.data["product_id"])
        title = get_data_or_none(request, "title")
        quantity = get_data_or_none(request, "quantity")
        subcategory_id = get_data_or_none(request, "subcategory_id")
    except Exception:
        return error("requiredParams")

    if not (title or subcategory_id or quantity):
        return error("requiredParams", {
            "message": "at least one of 'title', 'subcategory_id' or 'quantity 'must be passed"})

    if len(Product.objects.filter(title=title)):
        return error("notUniqueTitle")

    if not len(Product.objects.filter(id=product_id)):
        return error("productNotFound")
    if subcategory_id:
        if not len(SubCategory.objects.filter(id=subcategory_id)):
            return error("subcategoryNotFound")
    product = Product.objects.get(id=product_id)
    product.title = [title if title else product.title][0]
    product.quantity = [quantity if quantity else product.quantity][0]
    product.subCategory = [SubCategory.objects.get(id=subcategory_id) if subcategory_id
                           else product.subCategory][0]
    product.save()

    return Response({"message": "product edited successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_category(request):
    """
    Find category by id and DELETE it

    potential errors:
        requiredParams
        categoryNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(Category.objects.filter(id=id)):
        return error("categoryNotFound")
    category = Category.objects.get(id=id)
    category.delete()

    return Response({"message": "category deleted successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_subcategory(request):
    """
    Find subcategory by id and DELETE it

    potential errors:
        requiredParams
        subcategoryNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(SubCategory.objects.filter(id=id)):
        return error("subcategoryNotFound")
    subcategory = SubCategory.objects.get(id=id)
    subcategory.delete()

    return Response({"message": "subcategory deleted successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_product(request):
    """
    Find product by id and DELETE it

    potential errors:
        requiredParams
        productNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(Product.objects.filter(id=id)):
        return error("productNotFound")
    product = Product.objects.get(id=id)
    product.delete()

    return Response({"message": "product deleted successfully",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def the_category(request):
    """
    passes an specific category according to it's id

    potential errors:
        requiredParams
        categoryNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(Category.objects.filter(id=id)):
        return error("categoryNotFound")
    category = Category.objects.get(id=id)

    return Response(category_item(category),
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def the_subcategory(request):
    """
    passes an specific subcategory according to it's id

    potential errors:
        requiredParams
        subcategoryNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(SubCategory.objects.filter(id=id)):
        return error("subcategoryNotFound")
    subcategory = SubCategory.objects.get(id=id)

    return Response(subcategory_item(subcategory),
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def the_product(request):
    """
    passes an specific product according to it's id

    potential errors:
        requiredParams
        productNotFound
    """
    try:
        id = int(request.data["id"])
    except Exception:
        return error("requiredParams")

    if not len(Product.objects.filter(id=id)):
        return error("productNotFound")
    product = Product.objects.get(id=id)

    return Response(product_item(product),
                    status=status.HTTP_200_OK)
