from models import *
from getDbModel import *
from django.db.models import Q

def search(query):
	query       =    query.upper()
	searchTerms =    query.split()
	numTerms    = len(searchTerms)

	#exact matching case
	exactCrises = searchCrisis([query])
	exactPeople = searchPerson([query])
	exactOrgs   =      searchOrg([query])

	#or case
	orCrises = searchCrisis(searchTerms).difference(exactCrises)
	orPeople = searchPerson(searchTerms).difference(exactPeople)
	orOrgs   =      searchOrg(searchTerms).difference(exactOrgs)

	matchingCount = {}
	

	for crisis in orCrises:
		matchingCount[crisis.crisis_ID] = 0

	for person in orPeople:
		matchingCount[person.person_ID] = 0

	for org in orOrgs:
		matchingCount[org.org_ID] = 0

	print matchingCount

	# and case
	for crisis in orCrises:
		crisisString = str(getCrisis(crisis.crisis_ID)).upper()
		for term in searchTerms:
			if term in crisisString:
				matchingCount[crisis.crisis_ID] += 1

	for person in orPeople:
		personString = str(getPerson(person.person_ID)).upper()
		for term in searchTerms:
			if term in personString:
				matchingCount[person.person_ID] += 1

	for org in orOrgs:
		orgString = str(getOrg(org.org_ID)).upper()
		for term in searchTerms:
			if term in orgString:
				matchingCount[org.org_ID] += 1

	print matchingCount

	orSet = orCrises.union(orPeople)
	orSet = orSet.union(orOrgs)


	matches = orCrises.union(orPeople)
	matches = matches.union(orOrgs)
	return matches



def countIncrement(container, orObjects):
	found = False
	for object in orObjects:
		for match in matches:
			if object == match:
				object.count += 1
				found = True
		if not found:
			matches.add(i)

def searchCrisis(searchTerms) :
	modelSet = {}
	for term in searchTerms :
		modelSet = modelSet.union(Crisis.objects.filter(Q(crisis_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(date__iregex = term) | Q(time__iregex = term) | Q(common_summary__iregex = term)))	
	return modelSet
def searchPerson(searchTerms) :
	modelSet = {}
	for term in searchTerms :
		modelSet = modelSet.union(Person.objects.filter(Q(person_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))
	return modelSet			
def searchOrg(searchTerms) :
	modelSet = {}
	for term in searchTerms :
		modelSet = modelSet.union(Org.objects.filter(Q(org_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))
	return modelSet		

class match():
	def __init__(self, id):
		self.id = id
		self.context
		self.count
