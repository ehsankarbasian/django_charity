"""
hint:
this file is imported in views.py and classes below are used
as the input of @limiter([]) decorator for each @api_view

the classes here inherit UserRateLimiter (UserRateThrottle)

we used the word 'Limiter' instead 'Throttle' here ond in views.py just to be easy (-:
"""

from rest_framework.throttling import UserRateThrottle as UserRateLimiter


LOGIN_RATE = '15/minute'
SIGN_UP_RATE = '30/minute'
EMAIL_VERIFICATION_RATE = '80/minute'
LOG_OUT_RATE = '10/minute'
RESET_PASS_RATE = '20/minute'
FORGOT_PASS_RATE = '20/minute'
PROFILE_RATE = '100/minute'
BIO_RATE = '30/minute'
CREATE_EVENT_RATE = '30/minute'
EDIT_EVENT_RATE = '20/minute'
FEEDBACK_EVENT_RATE = '30/minute'
DISABLE_EVENT_RATE = '60/minute'
REQUESTED_EVENT_LIST_RATE = '40/minute'
SEARCH_RATE = '50/minute'
USER_EVENT_RATE = '30/minute'
DELETE_EVENT_BY_USER_RATE = '30/minute'
EDIT_EVENT_BY_USER_RATE = '20/minute'

"""
SIGN_UP_RATE is used for email verification too
"""


# Custom request_count limiter per time classes:
class LoginLimiter(UserRateLimiter):
    rate = LOGIN_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class SignUpLimiter(UserRateLimiter):
    rate = SIGN_UP_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class LogOutLimiter(UserRateLimiter):
    rate = LOG_OUT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class ForgotPasswordLimiter(UserRateLimiter):
    rate = FORGOT_PASS_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class ResetPasswordLimiter(UserRateLimiter):
    rate = RESET_PASS_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class ProfileLimiter(UserRateLimiter):
    rate = PROFILE_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class BioLimiter(UserRateLimiter):
    rate = BIO_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class CreateEventLimiter(UserRateLimiter):
    rate = CREATE_EVENT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class RequestedEventListLimiter(UserRateLimiter):
    rate = REQUESTED_EVENT_LIST_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class EditEventLimiter(UserRateLimiter):
    rate = EDIT_EVENT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class FeedbackEventLimiter(UserRateLimiter):
    rate = FEEDBACK_EVENT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class DisableEventLimiter(UserRateLimiter):
    rate = DISABLE_EVENT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class SearchLimiter(UserRateLimiter):
    rate = SEARCH_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class UserEventLimiter(UserRateLimiter):
    rate = USER_EVENT_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class DeleteEventByUserLimiter(UserRateLimiter):
    rate = DELETE_EVENT_BY_USER_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class EditEventByUserLimiter(UserRateLimiter):
    rate = EDIT_EVENT_BY_USER_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)
