from django.shortcuts import HttpResponse, render
from datetime import date

# Create your views here.


def hello_view(request):
    if request.method == 'GET':
        return HttpResponse("Hello! Its my project")


def now_date_view(request):
    if request.method == 'GET':
        return HttpResponse(date.today())


def goodbye_view(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye user!')