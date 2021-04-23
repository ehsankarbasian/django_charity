from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('ForgotPassword', views.forgotPassword),

    path('LoadUserProfile', views.loadUserProfile),
    path('SubmitUserProfile', views.submitUserProfile),
    path('UserBio', views.userBio),

    path('SendEmail', views.email),

    path('CreateEvent', views.createEvent),
    path('EditEventByAdmin', views.editEventByAdmin)
]
