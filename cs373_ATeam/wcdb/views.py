from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from loadModels import validate, populate_models

filled_models = None

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
  elif people_id == '2' :
    return render(request, 'wcdb/PER_GUZMAN.html')
  elif people_id == '3' :
    return render(request, 'wcdb/PER_TTHBLD.html')
  else :
    return HttpResponse('not such path')

def index(request):
  return render(request, 'wcdb/index.html')

def passwordValidate(pw_input):
  password = "ateam"
  print pw_input
  if password == pw_input:
    return True
  else:
    return False

def importView(request):
  form = XMLUploadForm()
  if request.method == 'POST':
    form = XMLUploadForm(request.POST, request.FILES)
    if form.is_valid() and passwordValidate(form.cleaned_data['password']):
      # process data
      upload = request.FILES['xmlfile']
      e_tree = validate(upload)
      if e_tree :
        filled_models = populate_models(e_tree)
        print "FILLED MODELS", filled_models
        print "CRISES"
        for crisis in filled_models["crises"] :
          print crisis.name
          print crisis.kind
          print crisis.date
          print crisis.time
          for location in crisis.locations :
            print "location", location.floating_text
          # for person in crisis.people :
          #   print person
        return render(request, 'wcdb/import.html', {'form': form, 'success': "Uploaded successfully!", 'password': False})
  return render(request, 'wcdb/import.html', {'form': form, 'success': False, 'password': "Password incorrect!"})
>>>>>>> 342036d0c28d4cb5ac9e54aa7dce3964549c1bee

def exportView(request) :
  output = "<WorldCrises><Crisis></Crisis><Crisis></Crisis></WorldCrises>"

  #call unloadModels.py w/ filled_models = {Crises : [], Orgs : [], Ppl : []}
  receive_import(global filled_models)

  return render(request, 'wcdb/Export.html', {'output': output})
  
class XMLUploadForm(forms.Form):
  xmlfile = forms.FileField()
  password = forms.CharField(max_length=8, widget=forms.PasswordInput) 
