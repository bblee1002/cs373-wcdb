from models import Crisis, Person, Org, Relations, Li
import collections

"""
Views.py renders the view specified by a url.
"""


def getCrisis(id):
  """
  Added for Phase2 implementation
  Returns dictionary of individual crisis data
  dict of form = 
  """
  crisis = Crisis.objects.get(crisis_ID = id)
  crisis_dict = {}

  # #Create keys of dict and give values
  crisis_dict['name'] = crisis.name

  # if person.kind is not None :
  crisis_dict['kind'] = crisis.kind

  # if person.location is not None :
  crisis_dict['date'] = crisis.date

  crisis_dict['time'] = crisis.time

  temp_person = []
  temp_orgs = []
  temp_list = Relations.objects.filter(crisis_ID = id)

  for a in temp_list :
    if a.person_ID != None:
      temp_person.append(a.person_ID)
    if a.org_ID != None:
      temp_orgs.append(a.org_ID)

  crisis_dict['people'] = temp_person
  crisis_dict['organizations'] = temp_orgs

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}

  temp_list = []
  temp_list = Li.objects.filter(model_id = id)

  for a in temp_list :
    common_dict[a.kind].append(a)

  crisis_dict['common'] = common_dict

  return crisis_dict

def getPerson(id):
  """
  Added for Phase2 implementation
  Accesses information about individ person from the db 
  Queries db using ID of person
  Returns dictionary of individual person data of form:
  {name : *, kind : *, location : *, crises : [], organizations : [], Common : ?}
  """
  #assumes all people have an id and name
  # assert person.person_ID != None
  # assert person.name != None

  #***needs to be hooked up
  #when back end is ready
  person = Person.objects.get(person_ID = id)
  print person
  person_dict = {}

  # #Create keys of dict and give values
  person_dict['name'] = person.name

  # if person.kind is not None :
  person_dict['kind'] = person.kind

  # if person.location is not None :
  person_dict['location'] = person.location

  temp_crisis = []
  temp_orgs = []
  temp_list = Relations.objects.filter(person_ID = id)

  for a in temp_list :
    if a.crisis_ID != None:
      temp_crisis.append(a.crisis_ID)
    if a.org_ID != None:
      temp_orgs.append(a.org_ID)

  person_dict['crises'] = temp_crisis
  person_dict['organizations'] = temp_orgs

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}

  temp_list = []
  temp_list = Li.objects.filter(model_id = id)

  for a in temp_list :
    common_dict[a.kind].append(a)

  person_dict['common'] = common_dict

  return person_dict


def getOrg(id):
  """
  Added for Phase2 implementation
  Returns dictionary of individual organization data
  dict of form = 
  """
  org = Org.objects.get(org_ID = id)
  print org
  org_dict = {}

  # #Create keys of dict and give values
  org_dict['name'] = org.name

  # if person.kind is not None :
  org_dict['kind'] = org.kind

  # if person.location is not None :
  org_dict['location'] = org.location

  temp_people = []
  temp_crisis = []
  temp_list = Relations.objects.filter(org_ID = id)

  for a in temp_list :
    if a.crisis_ID != None:
      temp_crisis.append(a.crisis_ID)
    if a.person_ID != None:
      temp_people.append(a.person_ID)

  org_dict['crises'] = temp_crisis
  org_dict['people'] = temp_people

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': []}

  temp_list = []
  temp_list = Li.objects.filter(model_id = id)

  for a in temp_list :
    common_dict[a.kind].append(a)

  org_dict['common'] = common_dict

  return org_dict

def getCrisisIDs():
  '''
  return {"crisis_ID": "crisisName"}
  returns a dict of the crisis IDs so that front-end can present correct url
  '''
  objects = Crisis.objects.all()
  ids = {}
  for o in objects:
    ids[o.crisis_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids

def getOrgIDs():
  '''
  return {"org_ID": "orgName"}
  returns a dict of the org IDs so that front-end can present correct url
  '''
  objects = Org.objects.all()
  ids = {}
  for o in objects:
    ids[o.org_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids

def getPeopleIDs():
  '''
  return {"person_ID": "personName"}
  returns a dict of the person IDs so that front-end can present correct url
  '''
  objects = Person.objects.all()
  ids = {}
  for o in objects:
    ids[o.person_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids
