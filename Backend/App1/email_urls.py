"""
What is this file?

here is a separated from App1/urls.py url pattern code
it uses another TOKEN_API which it is in Backend/urls.py

using EMAIL_TOKEN_API user can just access email_urls not more
when user receives an email from site, he/she will see the token so ...
... API limiters will be stronger for email APIs to handle brute force
"""

from django.urls import path
from . import views

urlpatterns = [
    path('ResetPassword', views.resetPassword),
    path('VerifyEmail', views.verifyEmailCodeBased),
    path('VerifyEmailTokenBased', views.verifyEmailTokenBased),
]
