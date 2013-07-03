# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello from views.py") #render(request, 'wcdb/index.html')
	
