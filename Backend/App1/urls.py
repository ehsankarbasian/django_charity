from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('LoadUserProfile', views.loadUserProfile),
    path('SubmitUserProfile', views.submitUserProfile),
    path('ForgotPassword', views.forgotPassword),
    path('UserBio', views.userBio),
]
