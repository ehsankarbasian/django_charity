"""
hint:
this file is imported in views.py and classes below are used
as the input of @limiter([]) decorator for each @api_view

the classes here inherit UserRateLimiter (UserRateThrottle)

we used the word 'Limiter' instead 'Throttle' here ond in views.py just to be easy (-:
"""

from rest_framework.throttling import UserRateThrottle as UserRateLimiter


LOGIN_RATE = '15/minute'
SIGN_UP_RATE = '3/minute'
LOG_OUT_RATE = '20/minute'
LOAD_PROFILE_RATE = '10/minute'
SUBMIT_PROFILE_RATE = '10/minute'


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


class LoadProfileLimiter(UserRateLimiter):
    rate = LOAD_PROFILE_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)


class SubmitProfileLimiter(UserRateLimiter):
    rate = SUBMIT_PROFILE_RATE

    def allow_request(self, request, view):
        return super().allow_request(request, view)
