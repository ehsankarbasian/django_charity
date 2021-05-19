"""
The functions below helps lister_functions.py

contains:
    user_item
    event_item
    category_item
    subcategory_item
    product_item
"""


def user_item(user):
    item = {
        "id": user.id,
        "username": user.user.username,
        "user_type": user.user_type,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "melli_code": user.melli_code,
        "email": user.email,
        "job": user.job,
        "address": user.address,
        "mobile_number": user.mobile_number,
        "house_phone": user.house_phone,
        "workplace_phone": user.workplace_phone,
        "gender": ["male" if user.gender == 1 else "female"][0],
        "married": user.married,
        "birth_date": user.birth_date
    }

    return item


def event_item(event):
    event_json = {}
    list_of_needs = {}

    if event.list_of_needs is None:
        list_of_needs = ""
    else:
        counter = 0
        for need in event.list_of_needs.split(","):
            counter += 1
            list_of_needs[counter] = need
    user = event.creator
    event_json[event.id] = {
        "status": event.status,
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "list_of_needs": list_of_needs,
        "feedback": [event.feedback if len(event.feedback) else None][0],
        "creator_username": user.username,
        "create_date": event.create_date,
        "image_url": event.image_url,
        "money_target": event.money_target,
        "donated_money": event.donated_money,
        "to_money_target": event.to_money_target(),
    }
    return event_json


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
