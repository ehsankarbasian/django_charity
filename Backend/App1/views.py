from rest_framework.decorators import throttle_classes as limiter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from App1.models import UserProfile
from App1.models import Event

from App1.Components.helper_functions import *
from App1.Components.custom_limiter import *

from App1.Components.APIs.auth_apis import *
from App1.Components.APIs.profile_apis import *
from App1.Components.APIs.event_apis import *


# API functions:
@api_view(['POST'])
def email(request):
    """
    It's an API to send email from ntm.patronage@gmail.com to a list

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
    except:
        return error("requiredParams")

    to_list = to_list.split(separated_with)
    send_text_email(subject, message, to_list)

    return Response({"message": "email sent",
                     "success": "1"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@limiter([SearchLimiter])
def search(request):
    PAGINATED_BY = 10
    """
    searches for events according to title and description
    just for 'enabled' & 'accepted' events
    it's not case-sensitive
    it paginates event by PAGINATED_BY

    potential errors:
        requiredParams
        pageOverFlowError
        noResultForSearch
    """
    try:
        search_key = request.data["search_key"]
        page_number = int(request.data["page_number"])
    except:
        return error("requiredParams")

    # Search:
    search_query = Q(title__contains=search_key) | Q(description__contains=search_key)
    allowed_event_query = Q(enabled=1) & Q(status=1)
    result_set = Event.objects.filter(search_query).filter(allowed_event_query)

    if not len(result_set):
        return error("noResultForSearch")

    # Paginate:
    paginator = Paginator(result_set, PAGINATED_BY)
    if page_number > paginator.num_pages:
        return error("pageOverFlowError", {"the_last_page": paginator.num_pages})
    page = paginator.page(page_number)

    return create_event_set(page, pagination_bar_params(page))
