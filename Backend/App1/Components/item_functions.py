"""
The functions below helps lister_functions.py

contains:
    user_item
    event_item
    category_item
    subcategory_item
    product_item
    transaction_item
    donateIn_item
"""


from App1.models import *


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
    list_of_needs = {}

    if event.list_of_needs is None:
        list_of_needs = ""
    else:
        counter = 0
        for need in event.list_of_needs.split(","):
            counter += 1
            list_of_needs[counter] = need
    user = event.creator
    event_json = {
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


def transaction_item(transaction):
    try:
        donate_in = DonatesIn.objects.get(transaction=transaction)
        event = donate_in.event
        event_title = event.title
        if event is not None:
            event_id = event.id
        else:
            event_id = None
    except Exception:
        event_id = None
        event_title = ""

    user = User.objects.get(user=transaction.donatorOrNeedy)

    item = {"id": transaction.id,
            "is_in": transaction.is_in,
            "amount": transaction.amount,
            "create_date": transaction.create_date,
            "user_id": transaction.donatorOrNeedy.id,
            "username": user.username,
            "event_id": event_id,
            "event_title": event_title}
    return item


def donateIn_item(donate):
    product = donate.product
    if product is not None:
        donator = donate.donator
        item = {"donate_id": donate.id,
                "product_name": product.title,
                "product_id": product.id,
                "quantity": donate.quantity,
                "melli_code": donator.melli_code,
                "donator_fname": donator.first_name,
                "donator_lname": donator.last_name}
    else:
        donator = donate.donator
        item = {"donate_id": donate.id,
                "product_name": "None",
                "product_id": "None",
                "quantity": donate.quantity,
                "melli_code": donator.melli_code,
                "donator_fname": donator.first_name,
                "donator_lname": donator.last_name}
    return item


def needRequest_item(needRequest):
    creator = needRequest.creator
    item = {"title": needRequest.title,
            "description": needRequest.description,
            "creator_username": creator.user.username,
            "creator_fname": creator.first_name,
            "creator_lname": creator.last_name}
    return item
