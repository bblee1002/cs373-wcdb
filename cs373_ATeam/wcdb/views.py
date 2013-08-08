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
from search import search

"""
Views.py renders the view specified by a url.
"""

# Renders html for a given crisis based on id given (crisis_id)
def crisisView(request, crisis_id):
  """
  Renders cri_temp.html with the information for a given crisis. The crisis to
  render is determined by crisis_id, whose value is passed to the function via
  the URL.

  @type request: HTML request
  @param request: An HTML request
  @type crisis_id: string
  @param crisis_id: a crisis ID that uniquely identifies a specific crisis.

  @rtype: HTML page
  @return: The rendered version of cri_temp.html
  """

  crisis_dict = getCrisis(crisis_id)

  return render(request, 'wcdb/cri_temp.html', crisis_dict)

# Renders html for a given org based on id given (orgs_id)
def orgsView(request, orgs_id):
  """
  Renders org_temp.html with the information for a given organization. The org
  to render is determined by orgs_id, whose value is passed to the function via
  the URL.

  @type request: HTML request
  @param request: An HTML request
  @type orgs_id: string
  @param orgs_id: an org ID that uniquely identifies a specific org.

  @rtype: HTML page
  @return: The rendered version of org_temp.html
  """

  org_dict = getOrg(orgs_id)
  return render(request, 'wcdb/org_temp.html', org_dict)

# Renders html for a given person based on id given (people_id)
def peopleView(request, people_id):
  """
  Renders per_temp.html with the information for a given person. The person to
  render is determined by people_id, whose value is passed to the function via
  the URL.

  @type request: HTML request
  @param request: An HTML request
  @type people_id: string
  @param people_id: a person ID that uniquely identifies a specific person.

  @rtype: HTML page
  @return: The rendered version of per_temp.html
  """

  per_dict = getPerson(people_id)

  return render(request, 'wcdb/per_temp.html', per_dict)

# Displays crises stored in the database. Which crises get displayed depends on kind of crisis selected.
def crisesPage(request, kind):
  """
  Renders crisesPage.html, which displays crises stored in the database. Which
  crises get displayed depends on the kind of crisis selected. The kind of
  crisis selected is determined by the value of kind, which is passed through
  the URL.

  @type request: HTML request
  @param request: An HTML request
  @type kind: string
  @param kind: Kind of crises to display.

  @rtype: HTML page
  @return: The rendered version of crisesPage.html
  """

  query_result_set = Crisis.objects.all()

  # Construct list of possible kinds
  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)

  # If kind selected is not "All" orgs, filter search results accordingly
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
  Renders orgPage.html, which displays organizations stored in the database.
  Which orgs get displayed depends on kind of org selected. The kind of org
  selected is determined by the value of kind, which is passed through the URL.

  @type request: HTML request
  @param request: An HTML request
  @type kind: string
  @param kind: Kind of organizations to display.

  @rtype: HTML page
  @return: The rendered version of orgPage.html
  """

  query_result_set = Org.objects.all()

  # Construct list of possible kinds
  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)

  # If kind selected is not "All" orgs, filter search results accordingly
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
  Renders pplPage.html, which displays people stored in the database. Which
  people get displayed depends on kind of person selected. The kind of person
  selected is determined by the value of kind, which is passed through the URL.

  @type request: HTML request
  @param request: An HTML request
  @type kind: string
  @param kind: Kind of people to display.

  @rtype: HTML page
  @return: The rendered version of pplPage.html
  """

  query_result_set = Person.objects.all()

  # Construct list of possible kinds
  kinds = ['All']
  for obj in query_result_set:
    found = False
    for kind_li in kinds:
      if kind_li.upper() == obj.kind.upper():
        found = True
    if not found:
      kinds.append(obj.kind)

  # If kind selected is not "All" people, filter search results accordingly
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
  Renders homepage.

  @type request: HTML request
  @param request: An HTML request

  @rtype: HTML page
  @return: Rendered version of index.html
  """

  return render(request, 'wcdb/index.html')

def unittestsView(request):
  """
  Runs the unit tests in tests.py and then renders Unittests.html, which
  displays the results of running those tests.

  @type request: HTML request
  @param request: An HTML request

  @rtype: HTML page
  @return: Rendered version of Unittests.html
  """

  output = subprocess.check_output(['python', 'manage.py', 'test', 'wcdb'],
    stderr=subprocess.STDOUT, shell=False)
  return render(request, 'wcdb/Unittests.html', {'output': output})

# Displays XML version of database information in browser
def exportView(request) :
  """
  Creates a string containing valid XML derived from the information stored in
  the database backing the website. Then renders Export.html using that string.
  Export.html displays the resulting string and offers user the option of
  downloading the information in the form of an XML file. Also writes exported
  string to a file named "WCDBExportXML.xml" which is stored locally on server.

  @type request: HTML request
  @param request: An HTML request

  @rtype: HTML page
  @return: Rendered version of Export.html
  """

  output = export_xml()

  return render(request, 'wcdb/Export.html', {'output': output})

# Downloads database information to user's computer as an XML file
def downloadView(request) :
  """
  Downloads the information in the database to the user's computer at the
  default download location in their browser settings. The file is an XML file.

  @type request: HTML request
  @param request: An HTML request

  @rtype: HttpResponse
  @return: HttpResponse containing XML file (named "wcdb.xml") as attachment.
  """

  response = HttpResponse('', mimetype="application/force-download")
  response.write(open('WCDBExportXML.xml', 'r').read())
  response['Content-Disposition'] = 'attachment; filename="wcdb.xml"'

  return response

def passwordValidate(pw_input, kind):
  """
  Helper function for importView. Validates the password for the Import
  facilities, returning true if the password was valid, and false otherwise.

  @type pw_input: string
  @param pw_input: password string the user entered
  @type kind: string
  @param kind: 
  """

  if pw_input == "ateam2" and kind == "clear" :
    return True
  elif pw_input == "ateam" and kind == "":
    return True
  else:
    return False

# Takes in an XML file and populates database accordingly
def importView(request, kind):
  """
  Renders import.html, which offers user the option to upload an XML file.
  Uploading an XML file requires the correct password, and the file itself
  will be validated to ensure not only that it is an XML file, but also that
  it matches the pre-defined schema for the website.
  """

  form = XMLUploadForm()
  if request.method == 'POST':
    form = XMLUploadForm(request.POST, request.FILES)

    if form.is_valid() and passwordValidate(form.cleaned_data['password'], kind):
      # process data
      upload = request.FILES['xmlfile']

      # validate XML file
      e_tree = validate(upload)
      if type(e_tree) == str:
        # XML file not valid
        return render(request, 'wcdb/import.html', {'form': form,
          'success': False, 'password': "", 'output': e_tree})

      # Valid XML file
      if e_tree :
        # Clear Database if Clear Import was selected and XML file was valid
        if kind == 'clear' :
          Crisis.objects.all().delete()
          Person.objects.all().delete()
          Org.objects.all().delete()
          Li.objects.all().delete()
          Relations.objects.all().delete()

        # Populate database
        populate_models(e_tree)

        return render(request, 'wcdb/import.html', {'form': form, 'success': "Uploaded successfully!", 'password': False})
  return render(request, 'wcdb/import.html', {'form': form, 'success': False, 'password': "Password incorrect!"})

def getTypeNameImage(idref) :
  '''
  Helper method for searchView. Returns a list in following format:
  [type of object, name, [LiObject, LiObject, ...] ] where LiObjects are Images
  '''

  if idref[0:3] == "CRI" :
    cri_instance = Crisis.objects.get(crisis_ID = idref)
    return ["crisis" , cri_instance.name, Li.objects.filter(kind = 'Images', model_id=idref)]
  if idref[0:3] == "PER" :
    per_instance = Person.objects.get(person_ID = idref)
    return ["person" , per_instance.name, Li.objects.filter(kind = 'Images', model_id=idref)]
  if idref[0:3] == "ORG" :
    org_instance = Org.objects.get(org_ID = idref)
    return ["org" , org_instance.name, Li.objects.filter(kind = 'Images', model_id=idref)]

def searchView(request):
  '''
  Renders search.html using the search results of a query entered
  into the search bar
  '''

  sform = SearchForm(request.POST)

  # Ensure form is valid
  if not sform.is_valid():
    return index(request)

  user_query = sform.cleaned_data['search_query']

  # Get search results. Format: [ MatchObject, MatchObject, ...]
  search_result = search(user_query)

  # Construct a dictionary from search results to pass along to html template
  search_dict = {"results" : [], "query" : ''}
  for match in search_result :
    # Make list for each MatchObject in search_result.
    # List format = [MatchObject, type of object, name of object, [LiObject, LiObject, ...] ]
    result_list = [match]
    result_list.extend(getTypeNameImage(match.idref))

    search_dict["results"].append(result_list)
  search_dict["query"] = sform.cleaned_data['search_query']

  return render(request, 'wcdb/search.html', search_dict)


def queriesView(request, query_num):
  '''
  Renders queries.html for the 10 selected queries (our 5 and 5 from other
  groups). query_num is a variable passed in the url that indicates which
  query to display.
  '''

  query_string = ''
  query_string1 = ''
  query_string2 = ''
  query_string3 = ''
  query_strings = []
  query_result_set = []
  query_dict = {}
  id_list = []
  set_of_unique_IDs = set([])

  # Convert query num from a string to an int
  try:
    query_num = int(query_num)
  except ValueError:
    query_num = 0

  # List of the 10 different queries, with 0 or 1 of them displaying, depending on the value of query_num
  if query_num == 1 :
    query_string =  "SELECT crisis_ID, name FROM (SELECT name, count(name) as Count, crisis_ID FROM wcdb_crisis c INNER JOIN wcdb_li l ON c.crisis_ID = l.model_id WHERE l.kind = 'Locations' GROUP BY crisis_ID, name ORDER BY Count DESC) AS sub LIMIT 1;"
    query_result_set = Crisis.objects.raw(query_string)

  elif query_num == 2 :
    query_string =  "SELECT crisis_ID, name, common_summary FROM wcdb_crisis WHERE crisis_ID in (SELECT model_id FROM (SELECT model_id, count(*) AS count FROM wcdb_li WHERE kind = 'Citations' GROUP BY model_id HAVING count >= 3) AS counts);"
    query_result_set = Crisis.objects.raw(query_string)

  elif query_num == 3 :
    query_string =  "SELECT id, model_id, floating_text, href FROM wcdb_li WHERE model_id in (SELECT org_ID FROM (SELECT org_ID, count(*) AS count FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID <> '' GROUP BY org_ID HAVING count >= 2) AS counter) AND kind = 'ContactInfo';"
    query_string1 = "SELECT id, model_id FROM wcdb_li WHERE model_id in (SELECT org_ID FROM (SELECT org_ID, count(*) AS count FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID <> '' GROUP BY org_ID HAVING count >= 2) AS counter) AND kind = 'ContactInfo';"
    query_string2 = "SELECT DISTINCT model_id FROM wcdb_li WHERE model_id in (SELECT org_ID FROM (SELECT org_ID, count(*) AS count FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID <> '' GROUP BY org_ID HAVING count >= 2) AS counter) AND kind = 'ContactInfo';"
    id_list = Li.objects.raw(query_string1)    
    for obj in id_list :
      set_of_unique_IDs.add(obj.model_id)
    query_result_set = (Li.objects.raw(query_string), set_of_unique_IDs)

  elif query_num == 4 :
    query_string =  "SELECT crisis_ID, name FROM wcdb_crisis WHERE date > '1990-01-01';"
    query_result_set = Crisis.objects.raw(query_string)

  elif query_num == 5 :
    query_string1 =  "SELECT crisis_ID, name,common_summary FROM wcdb_crisis WHERE crisis_ID = 'CRI_TXWDFR';"
    query_result_setC = Crisis.objects.raw(query_string1)
    query_string2 = "SELECT person_ID, name, common_summary FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations where person_ID <> '' AND crisis_ID = 'CRI_TXWDFR');"
    query_result_setP = Person.objects.raw(query_string2)
    query_string3 = "SELECT org_ID, name, common_summary FROM wcdb_org WHERE org_ID IN (SELECT DISTINCT org_ID FROM wcdb_relations where org_ID <> '' AND crisis_ID = 'CRI_TXWDFR');"
    query_result_setO = Org.objects.raw(query_string3)
    query_result_set = {"CrisisObjects" : query_result_setC, "PersonObjects" : query_result_setP, "OrgObjects" : query_result_setO}

  elif query_num == 6 :
    query_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations WHERE person_ID <> ''  AND crisis_ID IN(SELECT crisis_ID FROM wcdb_crisis WHERE date > '2000-01-01'));"
    query_result_set = Person.objects.raw(query_string)

  elif query_num == 7 :
    query_string =  "SELECT org_ID, name FROM wcdb_org WHERE org_ID IN (SELECT model_id FROM (SELECT model_id, count(*) AS count FROM wcdb_li WHERE kind = 'Videos' GROUP BY model_id HAVING count >= 2) AS counter);"
    query_result_set = Org.objects.raw(query_string)

  elif query_num == 8 :  
    query_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT person_ID FROM (SELECT person_ID, count(*) AS count FROM wcdb_relations WHERE person_ID <> '' AND crisis_ID <> '' GROUP BY person_ID HAVING count >= 2) AS counter);"
    query_result_set = Person.objects.raw(query_string)

  elif query_num == 9 :
    query_string =  "SELECT org_ID, name FROM wcdb_org WHERE org_ID IN (SELECT org_ID FROM wcdb_relations WHERE org_ID <> '' AND crisis_ID IN (SELECT crisis_ID FROM wcdb_crisis WHERE upper(kind) = 'NATURAL DISASTER'));"
    query_result_set = Org.objects.raw(query_string)

  elif query_num == 10 :
    query_string =  "SELECT person_ID, name FROM wcdb_person WHERE person_ID IN (SELECT DISTINCT person_ID FROM wcdb_relations WHERE person_ID <> '' AND person_ID <> 'PER_BROBMA' AND (crisis_ID IN (SELECT crisis_ID FROM wcdb_relations WHERE crisis_ID <> '' AND person_ID = 'PER_BROBMA') OR org_ID IN (SELECT org_ID FROM wcdb_relations WHERE org_ID <> '' AND person_ID = 'PER_BROBMA')))"
    query_result_set = Person.objects.raw(query_string)

  # The raw queries used are placed into a list of strings.
  query_strings.append(query_string)
  query_strings.append(query_string1)
  query_strings.append(query_string2)
  query_strings.append(query_string3)

  # This list, along with the result set of the query, are wrapped into a tuple and placed into
  # a dictionary, along with the value of query_num and the plain english version of the query.
  query_tuple = (query_strings, query_result_set)

  queries_dict = {"queries": {  "Show the crisis that is the most widespread (occurs in the most locations)." : 1, 
                                "Show the name and summary of crises with 3 or more citations (crises that are well-documented information-wise)." : 2,
                                "Show the ID and contact info for organizations associated with multiple crises." : 3,
                                "Show all crises that began after 1990 (recent crises)." : 4,
                                "Show the name and summary for the Texas Wildfire crisis and the name/summary for all people involved with it and the name/history of all organizations involved with it." : 5,
                                "Show all people involved in crises that happened in the 21st century." : 6,
                                "Show all organizations that have at least 2 related videos." : 7,
                                "Show all people linked to at least 2 crises." : 8,
                                "Show all organizations related to crises that are natural disasters." : 9,
                                "Show all people related to a crisis or organization that is related to Obama." : 10
                              },
                  "num" : query_num,
                  "results" : query_tuple,
                }
  return render(request, 'wcdb/queries.html', queries_dict)

class XMLUploadForm(forms.Form):
  """
  XMLUploadForm that has an upload file field along with a password field.
  Only present in import.html.
  """

  xmlfile = forms.FileField()
  password = forms.CharField(max_length=8, widget=forms.PasswordInput) 

class SearchForm(forms.Form):
  '''
  Form used in bar at top of every page (part of default.html, which every
  other html page extends) to post search queries. Contains a single field
  to store the query.
  '''
  
  search_query = forms.CharField(max_length = 200)