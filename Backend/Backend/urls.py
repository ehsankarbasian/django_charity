"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

TOKEN_API = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2MTg3MTYzOTEsImV"
EMAIL_TOKEN_API = "0xAjE2MT6eiOi538574I1NiJ467f4378A9iOiJ821A5IiLC695e6b88FFxkZ1a997F"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('App1/' + TOKEN_API + '/', include('App1.urls')),
    path('App1/' + EMAIL_TOKEN_API + '/', include('App1.email_urls')),

    # TODO: delete these after front matched
    path('App1/', include('App1.urls'))
]
