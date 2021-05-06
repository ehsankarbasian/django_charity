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
    path('GetEventRequested', views.requestedEventList),
    path('EditEventByAdmin', views.editEventByAdmin),
    path('EditEventByUser', views.editEventByUser),
    path('LeaveFeedback', views.leaveFeedback),
    path('DisableEvent', views.disableEvent),
    path('Search', views.search),
    path('UserEvent', views.userEvent),
    path('DeleteEvent', views.deleteEvent),
    path('NotVerifiedUserSet', views.notVerifiedUserSet),
    path('VerifyOrRejectUser', views.verifyOrRejectUser),
]
