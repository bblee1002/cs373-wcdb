from models import Crisis, Person, Org, Relations, Li
import collections

"""
Views.py renders the view specified by a url.
"""

def getLi(id):
  """
  Accesses information about specific list item from the db.

  @type id: string
  @param id: Model_id of the list item, used to query db
  
  @rtype: dictionary
  @return: individual list item's data of form: 
  {floating_text : [], model_id : *, kind: []}
  """
  try:
    list_items = Li.objects.filter(model_id = id)
  except:
    return {}

  li_dict = {}
  li_dict['floating_text'] = []
  li_dict['kind'] = []
  #li_dict['model_id'] = id

  # #Create keys of dict and give values
  for li in list_items:
    li_dict['floating_text'].append(li.floating_text)
    li_dict['kind'].append(li.kind)

  return li_dict

def getCrisis(id):
  """
  Accesses information about specific crisis from the db.

  @type id: string
  @param id: crisis_ID of the crisis item, used to query db

  @rtype: dictionary
  @return: individual crisis data of form:
  {name : *, kind : *, date : *, time : *, people : [], organizations : [], Common : ?}
  """
  try:
    crisis = Crisis.objects.get(crisis_ID = id)
  except:
    return {}

  crisis_dict = {}

  # #Create keys of dict and give values
  crisis_dict['name'] = crisis.name

  if crisis.kind is not None :
    crisis_dict['kind'] = crisis.kind

  if crisis.date is not None :
    crisis_dict['date'] = crisis.date

  if crisis.time is not None:
    crisis_dict['time'] = crisis.time

  temp_person = []
  temp_orgs = []
  relations = Relations.objects.filter(crisis_ID = id)

  for a in relations :
    if len(a.person_ID) != 0 :
      try:
        name = Person.objects.get(person_ID = a.person_ID).name
      except:
        name = ''
      temp_person.append((a.person_ID, name))
    if len(a.org_ID) != 0 :
      try:
        name = Org.objects.get(org_ID = a.org_ID).name
      except:
        name = ''
      temp_orgs.append((a.org_ID, name))

  crisis_dict['people'] = temp_person
  crisis_dict['organizations'] = temp_orgs

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': [],
                  'Summary': crisis.common_summary}

  li_list = Li.objects.filter(model_id = id)

  for a in li_list :
    if a.kind == "Feeds" :
      if a.embed[0:20] == "https://twitter.com/" :
        common_dict[a.kind].append([a, "Twitter", a.embed[20:]])
      elif a.embed[0:20] == "https://www.facebook" :
        common_dict[a.kind].append([a, "Facebook", a.embed[25:]])
      else :
        common_dict[a.kind].append([a, ''])
    else :
      common_dict[a.kind].append(a)

  crisis_dict['common'] = common_dict

  return crisis_dict

def getPerson(id):
  """
  Accesses information about individ person from the db

  @type id: string
  @param id: person_ID of the person item, used to query db

  @rtype: dictionary
  @return: individual person data of form:
  {name : *, kind : *, location : *, crises : [], organizations : [], Common : ?}
  """
  #assumes all people have an id and name
  # assert person.person_ID != None
  # assert person.name != None
  try:
    person = Person.objects.get(person_ID = id)
  except:
    return {}

  person_dict = {}

  # #Create keys of dict and give values
  person_dict['name'] = person.name

  if person.kind is not None :
    person_dict['kind'] = person.kind

  if person.location is not None :
    person_dict['location'] = person.location

  temp_crisis = []
  temp_orgs = []
  relations = Relations.objects.filter(person_ID = id)

  for a in relations :
    if len(a.crisis_ID) != 0 :
      try:
        name = Crisis.objects.get(crisis_ID = a.crisis_ID).name
      except:
        name = ''
      temp_crisis.append((a.crisis_ID, name))
    if len(a.org_ID) != 0 :
      try:
        name = Org.objects.get(org_ID = a.org_ID).name
      except:
        name = ''
      temp_orgs.append((a.org_ID, name))

  person_dict['crises'] = temp_crisis
  person_dict['organizations'] = temp_orgs

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': [],
                  'Summary': person.common_summary}

  li_list = Li.objects.filter(model_id = id)

  for a in li_list :
    if a.kind == "Feeds" :
      if a.embed[0:20] == "https://twitter.com/" :
        common_dict[a.kind].append([a, "Twitter", a.embed[20:]])
      elif a.embed[0:20] == "https://www.facebook" :
        common_dict[a.kind].append([a, "Facebook", a.embed[25:]])
      else :
        common_dict[a.kind].append([a, ''])
    else :
      common_dict[a.kind].append(a)

  person_dict['common'] = common_dict

  return person_dict


def getOrg(id):
  """
  Accesses information about individ organization from the db

  @type id: string
  @param id: org_ID of the org item, used to query db

  @rtype: dictionary
  @return: individual organization data of form:
  {name : *, kind : *, location : *, crises : [], people : [], Common : ?}
  """
  try:
    org = Org.objects.get(org_ID = id)
  except:
    return {}

  org_dict = {}

  # #Create keys of dict and give values
  org_dict['name'] = org.name

  if org.kind is not None :
    org_dict['kind'] = org.kind

  if org.location is not None :
    org_dict['location'] = org.location

  temp_people = []
  temp_crisis = []
  relations = Relations.objects.filter(org_ID = id)

  for a in relations :
    if len(a.crisis_ID) != 0 :
      try:
        name = Crisis.objects.get(crisis_ID = a.crisis_ID).name
      except:
        name = ''
      temp_crisis.append((a.crisis_ID, name))
    if len(a.person_ID) != 0:
      try:
        name = Person.objects.get(person_ID = a.person_ID).name
      except:
        name = ''
      temp_people.append((a.person_ID, name))

  org_dict['crises'] = temp_crisis
  org_dict['people'] = temp_people

  common_dict = {'Locations': [], 'HumanImpact': [], 'EconomicImpact': [], 
                  'ResourcesNeeded': [], 'WaysToHelp': [], 'History': [],
                  'ContactInfo': [], 'Citations': [], 'ExternalLinks': [],
                  'Images': [], 'Videos': [], 'Maps': [], 'Feeds': [], 
                  'Summary': org.common_summary}

  li_list = Li.objects.filter(model_id = id)

  for a in li_list :
    if a.kind == "Feeds" :
      if a.embed[0:20] == "https://twitter.com/" :
        common_dict[a.kind].append([a, "Twitter", a.embed[20:]])
      elif a.embed[0:20] == "https://www.facebook" :
        common_dict[a.kind].append([a, "Facebook", a.embed[25:]])
      else :
        common_dict[a.kind].append([a, ''])
    else :
      common_dict[a.kind].append(a)

  org_dict['common'] = common_dict

  return org_dict

def getCrisisIDs():
  """
  Finds all crises in the database

  @rtype: OrderedDict
  @return: all crisis_IDs and crisis names with IDs as keys and names as values
  """
  objects = Crisis.objects.all()
  ids = {}
  for o in objects:
    ids[o.crisis_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids

def getOrgIDs():
  """
  Finds all organizations in the database

  @rtype: OrderedDict
  @return: all org_IDs and org names with IDs as keys and names as values
  """
  objects = Org.objects.all()
  ids = {}
  for o in objects:
    ids[o.org_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids

def getPeopleIDs():
  """
  Finds all people in the database

  @rtype: OrderedDict
  @return: all person_IDs and person names with IDs as keys and names as values
  """
  objects = Person.objects.all()
  ids = {}
  for o in objects:
    ids[o.person_ID] = o.name
  ids = collections.OrderedDict(sorted(ids.items(), key=lambda t: t[1]))
  return ids
