from models import *
from getDbModel import *
from django.db.models import Q

def search(query):
	query       =    query.upper()
	searchTerms =    query.split()
	numTerms    = len(searchTerms)

	#exact matching case
	# print "EXACT CASES"
	exactCrises = searchCrisis([query])
	exactPeople = searchPerson([query])
	exactOrgs   =    searchOrg([query])
	exactLis    =     searchLi([query])

	result = []

	for item in exactCrises :
		match = Match(item.crisis_ID, numTerms)
		result.append(match)

	for item in exactPeople :
		match = Match(item.person_ID, numTerms)
		result.append(match)

	for item in exactOrgs :
		match = Match(item.org_ID, numTerms)
		result.append(match)

	for exactItem in exactLis :
		for resultItem in result :
			if resultItem.id != exactItem.model_id :
				match = Match(exactItem.model_id, numTerms)
				result.append(match)


	# print exactCrises
	# print exactPeople
	# print exactOrgs

	#or case
	# print "OR CASES"
	orCrises = searchCrisis(searchTerms).difference(exactCrises)
	orPeople = searchPerson(searchTerms).difference(exactPeople)
	orOrgs   =      searchOrg(searchTerms).difference(exactOrgs)
	orLis    =        searchLi(searchTerms).difference(exactLis)

	orSet = orCrises.union(orPeople)
	orSet = orSet.union(orOrgs)
	orSet = orSet.union(orLis)
	# print orCrises
	# print orPeople
	# print orOrgs

	matchFound = {}

	#matchingCount = {}

	# initializing lists of booleans for each ID
	for crisis in orCrises:
		matchFound[crisis.crisis_ID] = [False] * numTerms

	for person in orPeople:
		matchFound[person.person_ID] = [False] * numTerms

	for org in orOrgs:
		matchFound[org.org_ID] = [False] * numTerms

	for li in orLis:
		matchFound[li.model_id] = [False] * numTerms

	# for crisis in orCrises:
	# 	matchingCount[crisis.crisis_ID] = 0

	# for person in orPeople:
	# 	matchingCount[person.person_ID] = 0

	# for org in orOrgs:
	# 	matchingCount[org.org_ID] = 0

	# print matchingCount

	for crisis in orCrises:
		crisisString = str(getCrisis(crisis.crisis_ID)).upper()
		count = 0
		for term in searchTerms:
			if term in crisisString:
				matchFound[crisis.crisis_ID][count] = True
			count += 1
				#matchingCount[crisis.crisis_ID] += 1

	for person in orPeople:
		personString = str(getPerson(person.person_ID)).upper()
		count = 0
		for term in searchTerms:
			if term in personString:
				matchFound[person.person_ID][count] = True
			count += 1


	for org in orOrgs:
		orgString = str(getOrg(org.org_ID)).upper()
		count = 0
		for term in searchTerms:
			if term in orgString:
				matchFound[org.org_ID][count] = True
			count += 1

	#dependent on what paul decides to do
	for li in orLis:
		liString = str(getLi(li.model_id)).upper()
		count = 0
		for term in searchTerms:
			if term in liString:
				matchFound[li.model_id][count] = True
			count += 1

	print matchFound

	sortedCounts = []
	for i in xrange(numTerms):
		sortedCounts.append([])

	for idref in matchFound:
		count = 0
		for boolean in matchFound[idref]:
			if boolean:
				count += 1
		match = Match(idref, count)
		sortedCounts[count - 1].append(match)
	print sortedCounts


	# for item in matchingCount :
	# 	sortedCounts[matchingCount[item] - 1].append(item)

	# for index in reversed(xrange(numTerms)):
	# 	for innerSorted in sortedCounts[index] :
	# 		match = Match(innerSorted, index)
	# 		result.append(match)

	# print len(result)
	# print result

	# matches = orCrises.union(orPeople)
	# matches = matches.union(orOrgs)
	# return matches



# def countIncrement(container, orObjects):
# 	found = False
# 	for object in orObjects:
# 		for match in matches:
# 			if object == match:
# 				object.count += 1
# 				found = True
# 		if not found:
# 			matches.add(i)

def searchCrisis(searchTerms) :
	modelSet = set()
	for term in searchTerms :
		modelSet = modelSet.union(Crisis.objects.filter(Q(crisis_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(date__iregex = term) | Q(time__iregex = term) | Q(common_summary__iregex = term)))	
	return modelSet

def searchPerson(searchTerms) :
	modelSet = set()
	for term in searchTerms :
		modelSet = modelSet.union(Person.objects.filter(Q(person_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))
	return modelSet			

def searchOrg(searchTerms) :
	modelSet = set()
	for term in searchTerms :
		modelSet = modelSet.union(Org.objects.filter(Q(org_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))
	return modelSet	

def searchLi(searchTerms) :
	modelSet = set()
	for term in searchTerms :
		modelSet = modelSet.union(Li.objects.filter(Q(href__iregex = term) | Q(embed__iregex = term) | Q(text__iregex = term) | Q(floating_text__iregex = term)))
	return modelSet		

class Match():
	def __init__(self, id, count):
		self.id = id 
		self.count = count
		self.context = None
