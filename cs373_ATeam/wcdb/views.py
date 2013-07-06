from django import forms
from django.http import HttpResponse
from django.shortcuts import render

def crisisView(request, crisis_id):
  if crisis_id == '1':
    return render(request, 'wcdb/CRI_NSAWRT.html')
  elif crisis_id == '2':
    return render(request, 'wcdb/CRI_MEXDRG.html')
  elif crisis_id == '3':
    return render(request, 'wcdb/CRI_BEEDIE.html')
  else:
    return HttpResponse("no such path")

def orgsView(request, orgs_id):
  return HttpResponse('hello from orgs')

def peopleView(request, people_id):
  return HttpResponse('hello from people')

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
