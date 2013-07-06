from django import forms
from django.http import HttpResponse
from django.shortcuts import render

def crisisView(request, crisis_id):
  return HttpResponse('hello')

def index(request):
  return render(request, 'wcdb/index.html')

def importView(request):
  if request.method == 'POST':
    form = XMLUploadForm(request.POST, request.FILES)
    if form.is_valid():
      # process data
      return HttpResponse("uploaded")
  else:
    form = XMLUploadForm()

  return render(request, 'wcdb/import.html', {'form': form})
  
class XMLUploadForm(forms.Form):
  xmlfile = forms.FileField()
