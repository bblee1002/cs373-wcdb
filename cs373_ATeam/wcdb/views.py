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
  if orgs_id == '1' :
    return render(request, 'wcdb/ORG_NSAAAA.html')
  elif orgs_id == '2' :
    return render(request, 'wcdb/ORG_SINCAR.html')
  elif orgs_id == '3' :
    return render(request, 'wcdb/ORG_EPAAAA.html')
  else :
    return HttpResponse("not such path")

def peopleView(request, people_id):
  if people_id == '1' :
    return render(request, 'wcdb/PER_SNOWDN.html')
  else :
    return HttpResponse('not such path')

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

def exportView(request) :
  return render(request, 'wcdb/Export.html')
  
class XMLUploadForm(forms.Form):
  xmlfile = forms.FileField()
