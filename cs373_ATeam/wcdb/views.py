from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from loadModels import validate, populate_models
from unloadModels import receive_import

imported_models = {}

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

def unittestsView(request):
  return render(request, 'wcdb/Unittests.html')

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
        #populate models returns a dictionary where the keys are 'crises', 'organizations' , 'people'
        #and the values are corresponding lists of crisis, organization, and person models
        #filled_models = populate_models(e_tree)
        global imported_models
        imported_models = populate_models(e_tree)
        return render(request, 'wcdb/import.html', {'form': form, 'success': "Uploaded successfully!", 'password': False})
  return render(request, 'wcdb/import.html', {'form': form, 'success': False, 'password': "Password incorrect!"})

def exportView(request) :
  output = "You have to import something before you export!"
  global imported_models
  if imported_models != {}:
    output = receive_import(imported_models)

  return render(request, 'wcdb/Export.html', {'output': output})
  
class XMLUploadForm(forms.Form):
  xmlfile = forms.FileField()
  password = forms.CharField(max_length=8, widget=forms.PasswordInput) 
