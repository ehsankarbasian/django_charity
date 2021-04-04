from django.urls import path, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('LoadUserProfile', views.LoadUserProfile),
    path('SubmitUserProfile', views.SubmitUserProfile),
]
