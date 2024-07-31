from django.shortcuts import render
# Create your views here.


# view function takkes a reques and returns a response 
# a device that responses things

# sample1/views.py

# backend/sample1/views.py
from django.http import HttpResponse

def hello_view(request):
    return HttpResponse("Hello")


    #pull data from db
    #transform data

    #send email
    #now map this to a url

