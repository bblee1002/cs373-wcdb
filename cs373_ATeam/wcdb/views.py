from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from loadModels import validate, populate_models
from unloadModels import receive_import
import subprocess

"""
Views.py renders the view specified by a url.
"""

imported_models = {}

def getCrisis(crisis):
  """
   Added for Phase2 implementation
  Returns dictionary of individual crisis data
  dict of form = 
  """

def getPerson(person):
  """
  Added for Phase2 implementation
  Returns dictionary of individual person data
  person_dict = {name : *, kind : *, location : *, crises : [], organizations : [], Common : ?}
  """
  #assumes all people have an id and name
  assert person.person_ID != None
  assert person.name != None

  person_dict = {}

  #Create keys of dict and give values
  person_dict[name] = person.name

  if person.kind is not None :
    person_dict[kind] = person.kind

  if person.location is not None :
    person_dict[location] = person.location

  #if there are crises listed
  if person.crises        != [] :
    temp_c = []
    #*****************************
    #Collect crisis ids into a list
    for c in person.crises :
      print c
      #temp_c += c.crisis_ID
    #person_dict[crises] = temp_c
  
  #if there are orgs listed
  if person.organizations != [] :
    temp_o = []
    for o in person.organizations :
      #*****************************
      print o
      #temp_o += o.org_ID
    #person_dict[organizations] = o
  
  # #Export info from the common class == how? new common function?
  # if person.common is not None :
  #   #person_string += person.common.print_xml()

  #Conclude person dictionary
  return person_dict


def getOrg(org):
  """
   Added for Phase2 implementation
  Returns dictionary of individual organization data
  dict of form = 
  """

def unpackDict():
  """
  Added for Phase2 implementation
  Unpacks the dictionary returned from import
  such that each model instance can be individually accessed
  """
  global imported_models
  #******make sure dictionary is filled by import at this point
  #assert len(imported_models) >= 0
  for c in imported_models[crises]:
    #iterate over crisis models
    getCrisis(c)
  for p in imported_models[people]:
    #iterate over person models
    getPerson(p)
  for o in imported_models[organizations]:
    #iterate over org models
    getOrg(o)


def crisisView(request, crisis_id):
  """
  Renders view for crises.
  """
  '''
  {'name': name, 'kind': kind, 'date': data, ...}
  '''
  if crisis_id == '1':
    return render(request, 'wcdb/CRI_NSAWRT.html')
  elif crisis_id == '2':
    return render(request, 'wcdb/CRI_MEXDRG.html')
  elif crisis_id == '3':
    return render(request, 'wcdb/CRI_BEEDIE.html')
  else:
    return HttpResponse("no such path")

def orgsView(request, orgs_id):
  """
  Renders view for organizations.
  """
  if orgs_id == '1' :
    return render(request, 'wcdb/ORG_NSAAAA.html')
  elif orgs_id == '2' :
    return render(request, 'wcdb/ORG_SINCAR.html')
  elif orgs_id == '3' :
    return render(request, 'wcdb/ORG_EPAAAA.html')
  else :
    return HttpResponse("not such path")

def peopleView(request, people_id):
  """
  Renders view for people.
  """
  if people_id == '1' :
    return render(request, 'wcdb/PER_SNOWDN.html')
  elif people_id == '2' :
    return render(request, 'wcdb/PER_GUZMAN.html')
  elif people_id == '3' :
    return render(request, 'wcdb/PER_TTHBLD.html')
  else :
    return HttpResponse('not such path')

def index(request):
  """
  Renders view for homepage.
  """
  return render(request, 'wcdb/index.html')

def unittestsView(request):
  """
  Renders view for unit tests as well as runs the unit tests.
  """
  output = subprocess.check_output(['python', 'manage.py', 'test', 'wcdb'],
    stderr=subprocess.STDOUT, shell=False)
  return render(request, 'wcdb/Unittests.html', {'output': output})

def passwordValidate(pw_input):
  """
  Validates that the password for the XMLUploadForm is correct.
  """
  password = "ateam"
  if password == pw_input:
    return True
  else:
    return False

def importView(request):
  """
  Renders view for import page, kicks off the import facility, reports
  back to the user success or failure.
  """
  form = XMLUploadForm()
  if request.method == 'POST':
    form = XMLUploadForm(request.POST, request.FILES)
    if form.is_valid() and passwordValidate(form.cleaned_data['password']):
      # process data
      upload = request.FILES['xmlfile']
      e_tree = validate(upload)
      if type(e_tree) == str:
        return render(request, 'wcdb/import.html', {'form': form,
          'success': False, 'password': "", 'output': e_tree})
      if e_tree :
        #populate models returns a dictionary where the keys are 'crises', 'organizations' , 'people'
        #and the values are corresponding lists of crisis, organization, and person models
        #filled_models = populate_models(e_tree)
        global imported_models
        imported_models = populate_models(e_tree)

        return render(request, 'wcdb/import.html', {'form': form, 'success': "Uploaded successfully!", 'password': False})
  return render(request, 'wcdb/import.html', {'form': form, 'success': False, 'password': "Password incorrect!"})

def exportView(request) :
  """
  Renders view for export page, kicks off export facility.
  """
  output = "You have to import something before you export!"
  global imported_models
  if imported_models != {}:
    output = receive_import(imported_models)

  return render(request, 'wcdb/Export.html', {'output': output})
  
class XMLUploadForm(forms.Form):
  """
  XMLUploadForm that has an upload file field along with a password field.
  """
  xmlfile = forms.FileField()
  password = forms.CharField(max_length=8, widget=forms.PasswordInput) 
