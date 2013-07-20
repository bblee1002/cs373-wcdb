from models import Crisis, Person, Org

"""
Views.py renders the view specified by a url.
"""


def getCrisis(id):
  """
  Added for Phase2 implementation
  Returns dictionary of individual crisis data
  dict of form = 
  """
  pass

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
  #person_model = Person.object.Filter(pid = id)

  person_dict = {}

  # #Create keys of dict and give values
  # person_dict[name] = person.name

  # if person.kind is not None :
  #   person_dict[kind] = person.kind

  # if person.location is not None :
  #   person_dict[location] = person.location

  # #if there are crises listed
  # if person.crises        != [] :
  #   temp_c = []
  #   #*****************************
  #   #Collect crisis ids into a list
  #   for c in person.crises :
  #     print c
  #     #temp_c += c.crisis_ID
  #   #person_dict[crises] = temp_c
  
  # #if there are orgs listed
  # if person.organizations != [] :
  #   temp_o = []
  #   for o in person.organizations :
  #     #*****************************
  #     print o
  #     #temp_o += o.org_ID
  #   #person_dict[organizations] = o
  
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
  pass

def getCrisisIDs():
  '''
  return {"crisisName": "id"}
  returns a dict of the crisis IDs so that front-end can present correct url
  '''
  pass

def getOrgIDs():
  '''
  return {"orgName": "id"}
  returns a dict of the org IDs so that front-end can present correct url
  '''
  pass

def getPeopleIDs():
  '''
  return {"personName": "id"}
  returns a dict of the person IDs so that front-end can present correct url
  '''
  pass
