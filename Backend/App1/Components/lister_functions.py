"""
The functions that adapts a queryset in JSONs to use by frontend

contains:
    category_item
    subcategory_item
    product_item

    category_lister
    subcategory_lister
    product_lister
"""


from rest_framework.response import Response
from rest_framework import status


def category_item(category):
    item = {"id": category.id,
            "title": category.title}

    return item


def subcategory_item(subcategory):
    item = {"id": subcategory.id,
            "title": subcategory.title,
            "category_title": subcategory.category.title,
            "category_id": subcategory.category.id}

    return item


def product_item(product):
    item = {"id": product.id,
            "title": product.title,
            "quantity": product.quantity,

            "subcategory_title": product.subCategory.title,
            "subcategory_id": product.subCategory.id,
            "category_title": product.subCategory.category.title,
            "category_id": product.subCategory.category.id}

    return item


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
                  "category_set": subcategory_json}

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
                  "category_set": product_json}

    return Response(final_json,
                    status=status.HTTP_200_OK)
