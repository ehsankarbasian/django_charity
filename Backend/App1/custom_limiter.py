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
RESET_PASS_RATE = '20/hour'
FORGOT_PASS_RATE = '2/minute'
PROFILE_RATE = '10/minute'

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
