from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from loadModels import validate, populate_models
from unloadModels import export_xml
from models import *
import subprocess
from getDbModel import  getCrisisIDs, getOrgIDs, getPeopleIDs
from getDbModel import getCrisis, getPerson, getOrg
import collections
from models import *

"""
Views.py renders the view specified by a url.
"""

imported_models = {}

def crisisView(request, crisis_id):
  """
  Renders view for crises.
  """
  crisis_dict = getCrisis(crisis_id)

  return render(request, 'wcdb/cri_temp.html', crisis_dict)

def orgsView(request, orgs_id):
  """
  Renders view for organizations.
  """
  org_dict = getOrg(orgs_id)
  # if len(org_dict) <= 0
  #   return HttpResponse('org does not exist')
  return render(request, 'wcdb/org_temp.html', org_dict)


def peopleView(request, people_id):
  """
  Renders view for people.
  """
  per_dict = getPerson(people_id)
  # if len(per_dict) == 0
  #   return HttpResponse('person does not exist')
  return render(request, 'wcdb/per_temp.html', per_dict)

def crisesPage(request, kind):
  """
  Displays all imported crises. 
  """

  query_result_set = Crisis.objects.all()
  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)
  if kind != 'All' :
    query_result_set = Crisis.objects.filter(kind=kind)
    for obj in query_result_set:
      print "KIND: " + obj.kind

  crisisIDs = {}
  for cri_obj in query_result_set :
    crisisIDs[cri_obj.crisis_ID] = (cri_obj,)

  for crisis in crisisIDs.items() :
    liObjects = Li.objects.filter(kind = 'Images', model_id=(crisis[1])[0].crisis_ID)
    summary = (crisis[1])[0].common_summary[0:101] + '...'
    if len(liObjects) != 0 :
      crisisIDs[(crisis[1])[0].crisis_ID] += ((liObjects[0]).embed, summary)
    else :
      crisisIDs[(crisis[1])[0].crisis_ID] += ('/static/img/whitespace.jpg', summary)

  return render(request, 'wcdb/crisesPage.html', {'crisisIDs' : crisisIDs, 'kinds' : kinds})

def orgPage(request, kind):
  """
  Displays all imported organizations. 
  """

  query_result_set = Org.objects.all()

  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)
  if kind != 'All' :
    query_result_set = Org.objects.filter(kind=kind)
    for obj in query_result_set:
      print "KIND: " + obj.kind

  orgIDs = {}
  for org_obj in query_result_set :
    orgIDs[org_obj.org_ID] = (org_obj,)

  for org in orgIDs.items() :
    liObjects = Li.objects.filter(kind = 'Images', model_id=(org[1])[0].org_ID)
    summary = (org[1])[0].common_summary[0:101] + '...'
    if len(liObjects) != 0 :
      orgIDs[(org[1])[0].org_ID] += ((liObjects[0]).embed, summary)
    else :
      orgIDs[(org[1])[0].org_ID] += ('/static/img/whitespace.jpg', summary)

  return render(request, 'wcdb/orgPage.html', {'orgIDs': orgIDs, 'kinds' : kinds})

def pplPage(request, kind):
  """
  Displays all imported people. 
  """

  query_result_set = Person.objects.all()

  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)
  if kind != 'All' :
    query_result_set = Person.objects.filter(kind=kind)
    for obj in query_result_set:
      print "KIND: " + obj.kind

  peopleIDs = {}
  for per_obj in query_result_set :
    peopleIDs[per_obj.person_ID] = (per_obj,)

  for person in peopleIDs.items() :
    liObjects = Li.objects.filter(kind = 'Images', model_id=(person[1])[0].person_ID)
    summary = (person[1])[0].common_summary[0:101] + '...'
    if len(liObjects) != 0 :
      peopleIDs[(person[1])[0].person_ID] += ((liObjects[0]).embed, summary)
    else :
      peopleIDs[(person[1])[0].person_ID] += ('/static/img/whitespace.jpg', summary)

  return render(request, 'wcdb/pplPage.html', {'peopleIDs': peopleIDs, 'kinds': kinds})

def index(request):
  """
  Renders view for homepage.
  """
  crisisIDs = getCrisisIDs()
  orgIDs = getOrgIDs()
  peopleIDs = getPeopleIDs()
  return render(request, 'wcdb/index.html', {'crisisIDs': crisisIDs,
    'orgIDs': orgIDs, 'peopleIDs': peopleIDs})

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


def exportView(request) :
  """
  Renders view for export page, kicks off export facility.
  """
  # output = "You have to import something before you export!"
  # global imported_models
  # if imported_models != {}:
  #   output = receive_import(imported_models)

  output = export_xml()

  return render(request, 'wcdb/Export.html', {'output': output})

def downloadView(request) :
  """
  Returns an XML document of what is in the models.
  """
  response = HttpResponse('', mimetype="application/force-download")
  response.write(open('WCDBExportXML.xml', 'r').read())
  response['Content-Disposition'] = 'attachment; filename="wcdb.xml"'

  return response

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

        #populate models should be changed to not return anything
        #everything that used to be returned by the dict should be accessed through the db
        #global imported_models
        #imported_models = populate_models(e_tree)
        populate_models(e_tree)
        #Dynamically access model data from the db instead of using dict at this point
        

        return render(request, 'wcdb/import.html', {'form': form, 'success': "Uploaded successfully!", 'password': False})
  return render(request, 'wcdb/import.html', {'form': form, 'success': False, 'password': "Password incorrect!"})

def searchView(request):
  sform = SearchForm(request.POST)
  if not sform.is_valid():
    return index(request)
  return render(request, 'wcdb/search.html', {"query": sform.cleaned_data['search_query']})

def queriesView(request):
  query1_string =  "SELECT crisis_ID, name FROM (SELECT name, count(name) as Count, crisis_ID FROM wcdb_crisis c INNER JOIN wcdb_li l ON c.crisis_ID = l.model_id WHERE l.kind = 'Locations' GROUP BY name ORDER BY Count DESC) AS sub LIMIT 1;"
  query_result_set = Crisis.objects.raw(query1_string)
  query1_tuple = (query1_string, query_result_set)

  query2_string =  "SELECT crisis_ID, name, common_summary FROM wcdb_crisis WHERE crisis_ID in (SELECT model_id FROM (SELECT model_id, count(*) AS count FROM wcdb_li WHERE kind = 'Citations' GROUP BY model_id HAVING count >= 3) AS counts);"
  query_result_set = Crisis.objects.raw(query2_string)
  query2_tuple = (query2_string, query_result_set)

  # query3_string =  "SELECT model_id, floating_text FROM wcdb_li WHERE model_id in (SELECT org_ID FROM (SELECT org_ID, count(*) AS count FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID <> '' GROUP BY org_ID HAVING count >= 2) AS counter) AND kind = 'ContactInfo';"
  # query_result_set = Li.objects.raw(query3_string)
  # query3_tuple = (query3_string, query_result_set)

  query4_string =  "SELECT crisis_ID, name FROM wcdb_crisis WHERE date > '1990-01-01';"
  query_result_set = Crisis.objects.raw(query4_string)
  query4_tuple = (query4_string, query_result_set)

  # query5_stringC =  "SELECT crisis_ID, name,common_summary FROM wcdb_crisis WHERE crisis_ID = 'CRI_TXWDFR';"
  # query_result_setC = Crisis.objects.raw(query5_stringC)
  # query5_stringP = "SELECT person_ID, name, common_summary FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations where person_ID <> '' AND crisis_ID = 'CRI_TXWDFR');"
  # query_result_setP = Person.objects.raw(query5_stringP)
  # query5_stringO = "SELECT org_ID, name, common_summary FROM wcdb_org WHERE org_ID IN (SELECT DISTINCT org_ID FROM wcdb_relations where org_ID <> '' AND crisis_ID = 'CRI_TXWDFR');"
  # query_result_setO = Org.objects.raw(query5_stringO)
  # query5_dict = {"CrisisObjects" : query_result_setC, "PersonObjects" : query_result_setP, "OrgObjects" : query_result_setO}
  # query1_tuple = (query1_string, query_result_set)

  query6_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations WHERE person_ID <> ''  AND crisis_ID IN(SELECT crisis_ID FROM wcdb_crisis WHERE date > '2000-01-01'));"
  query_result_set = Person.objects.raw(query6_string)
  query6_tuple = (query6_string, query_result_set)

  query7_string =  "SELECT org_ID, name FROM wcdb_org WHERE org_ID IN (SELECT model_id FROM (SELECT model_id, count(*) AS count FROM wcdb_li WHERE kind = 'Videos' GROUP BY model_id HAVING count >= 2) AS counter);"
  query_result_set = Org.objects.raw(query7_string)
  query7_tuple = (query7_string, query_result_set)
  
  query8_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT person_ID FROM (SELECT person_ID, count(*) AS count FROM wcdb_relations WHERE person_ID <> '' AND crisis_ID <> '' GROUP BY person_ID HAVING count >= 2) AS counter);"
  query_result_set = Person.objects.raw(query8_string)
  query8_tuple = (query8_string, query_result_set)
  
  query9_string =  "SELECT org_ID, name FROM wcdb_org WHERE org_ID IN (SELECT org_ID FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID IN (SELECT crisis_ID FROM wcdb_crisis WHERE upper(kind) = 'NATURAL DISASTER'));"
  query_result_set = Org.objects.raw(query9_string)
  query9_tuple = (query9_string, query_result_set)
  
  query10_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations WHERE person_ID <> '' AND person_ID <> 'PER_ESNWDN' AND (crisis_ID IN (SELECT crisis_ID FROM wcdb_relations WHERE crisis_ID <> '' AND person_ID = 'PER_ESNWDN') OR org_ID IN (SELECT org_ID FROM wcdb_relations WHERE org_ID <> '' AND person_ID = 'PER_ESNWDN')))"
  query_result_set = Person.objects.raw(query10_string)
  query10_tuple = (query10_string, query_result_set)

  queries_dict = {"queries_dict": { "Show the crisis that is the most widespread (occurs in the most locations)." : query1_tuple, 
                                    "Show the name and summary of crises with 3 or more citations (crises that are well-documented information-wise)." : query2_tuple,
                                    # "Show the ID and contact info for organizations associated with multiple crises." : query3_tuple,
                                    "Show all crises that began after 1990 (recent crises)." : query4_tuple,
                                    # "Show the name and summary for the Texas Wildfire crisis and the name/summary for all people involved with it and the name/history of all organizations involved with it." : query5_tuple,
                                    "Show all people involved in crises that happened in the 21st century." : query6_tuple,
                                    "Show all organizations that have at least 2 related videos." : query7_tuple,
                                    "Show all people linked to at least 2 crises." : query8_tuple,
                                    "Show all organizations related to crises that are natural disasters." : query9_tuple,
                                    "Show all people related to a crisis or organization that is related to Obama." : query10_tuple,
                                    } }
  return render(request, 'wcdb/queries.html', queries_dict)

class XMLUploadForm(forms.Form):
  """
  XMLUploadForm that has an upload file field along with a password field.
  """
  xmlfile = forms.FileField()
  password = forms.CharField(max_length=8, widget=forms.PasswordInput) 

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length = 200)