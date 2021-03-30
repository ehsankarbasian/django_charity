from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login (request):
    return HttpResponse("Log in page will be here.")

def signup (request):
    return HttpResponse("Sign up page will be here.")