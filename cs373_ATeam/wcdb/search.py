from models import *
from getDbModel import *
from django.db.models import Q
import re


def search(query) :
	query       =    query.upper()
	searchTerms =    query.split()
	numTerms    = len(searchTerms)
	result      =               []

	#exact matching case
	exactCrises = searchCrisis([query])
	exactPeople = searchPerson([query])
	exactOrgs   =    searchOrg([query])
	exactLis    =     searchLi([query])


	for item in exactCrises :
		match = Match(item.crisis_ID, numTerms)
		result.append(match)

	for item in exactPeople :
		match = Match(item.person_ID, numTerms)
		result.append(match)

	for item in exactOrgs :
		match = Match(item.org_ID, numTerms)
		result.append(match)

	for item in exactLis :
		repeat = False
		for resultItem in result :
			if resultItem.idref == item.model_id :
				repeat = True
				break
		if repeat == False :
			match = Match(item.model_id, numTerms)
			result.append(match)
	#or case
	orCrises = searchCrisis(searchTerms).difference(exactCrises)
	orPeople = searchPerson(searchTerms).difference(exactPeople)
	orOrgs   =      searchOrg(searchTerms).difference(exactOrgs)
	orLis    =        searchLi(searchTerms).difference(exactLis)
	
	for li in searchLi(searchTerms).difference(exactLis) :
		repeat = False
		for resultItem in result :
			if li.model_id == resultItem.idref :
				orLis.remove(li)


	matchFound = {}
	# initializing lists of booleans for each ID
	initMatchFound(numTerms, matchFound, orCrises, orPeople, orOrgs, orLis)
	#populating the dictionary
	populateMatchFound(searchTerms, numTerms, matchFound, orCrises, orPeople, orOrgs, orLis)

	print matchFound

	sortedCounts = []
	for i in xrange(numTerms) :
		sortedCounts.append([])

	for idref in matchFound:
		count = 0
		for boolean in matchFound[idref]:
			if boolean:
				count += 1
		match = Match(idref, count)
		sortedCounts[count - 1].append(match)

	# print "BEFORE ADDING ORS"
	# for res in result :
	# 	print res.id
	for index in reversed(xrange(numTerms)) :
		for match in sortedCounts[index] :
			result.append(match)
	#print result
	# print "\nAFTER ADDING ORS"
	# for res in result :
	# 	print res.id
	getContext(result, matchFound, searchTerms, numTerms)
	for match in result:
		for context in match.contexts:
			print "begin: ", context.begin 
			print "bold: ", context.bold 
			print "end: ", context.end


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

def initMatchFound(numTerms, matchFound, orCrises, orPeople, orOrgs, orLis) :
	for crisis in orCrises:
		matchFound[crisis.crisis_ID] = [False] * numTerms

	for person in orPeople:
		matchFound[person.person_ID] = [False] * numTerms

	for org in orOrgs:
		matchFound[org.org_ID] = [False] * numTerms

	for li in orLis:
		matchFound[li.model_id] = [False] * numTerms

def populateMatchFound(searchTerms, numTerms, matchFound, orCrises, orPeople, orOrgs, orLis) :
	for crisis in orCrises:
		crisisString = str(getCrisis(crisis.crisis_ID)).upper()
		count = 0
		for term in searchTerms:
			if term in crisisString:
				matchFound[crisis.crisis_ID][count] = True
			count += 1

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

	for li in orLis:
		liString = str(getLi(li.model_id)).upper()
		count = 0
		for term in searchTerms:
			if term in liString:
				matchFound[li.model_id][count] = True
			count += 1

def getContext(result, matchFound, searchTerms, numTerms):
	for match in result :
		# iterate through model:
		#crisis_dict = {name : *, kind : *, date : *, time : *, people : [], organizations : [], Common : ?}
		if match.idref[0:3] == "CRI" :
			modelDict = getCrisis(match.idref)
			

			for index in xrange(numTerms) :
				if matchFound[match.idref][index] == False :
					continue

				found = modelDict['name'].upper().find(searchTerms[index])
				if found >= 0 :
					tempContext = Context()
					tempContext.begin =  'NAME...'
					if found > 0 :
						regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['name'][found-1::-1]).group(0)
						print "SUBSTRING: ", modelDict['name'][found-1::-1]
						print "BEFORE CONCATENATION: ", regex
						tempContext.begin += regex[::-1]
						print "TESTING: ", tempContext.begin
					tempContext.bold  =  modelDict['name'][found:(found + len(searchTerms[index]))]
					tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['name'][found + len(searchTerms[index]): found + 100]).group(0)
					match.contexts.append(tempContext)
					continue

				found = modelDict['kind'].upper().find(searchTerms[index])
				if found >= 0 :
					tempContext = Context()
					tempContext.begin =  'KIND...'
					if found > 0 :
						regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['kind'][found-1::-1]).group(0)
						tempContext.begin += regex[::-1]
					tempContext.bold  =  modelDict['kind'][found:(found + len(searchTerms[index]))]
					tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['kind'][found + len(searchTerms[index]): found + 100]).group(0)
					match.contexts.append(tempContext)
					continue

				found = modelDict['date'].upper().find(searchTerms[index])
				if found >= 0 :
					tempContext = Context()
					tempContext.begin =  'DATE...'
					if found > 0 :
						regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['date'][found-1::-1]).group(0)
						tempContext.begin += regex[::-1]
					tempContext.bold  =  modelDict['date'][found:(found + len(searchTerms[index]))]
					tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['date'][found + len(searchTerms[index]): found + 100]).group(0)
					match.contexts.append(tempContext)
					continu

				found = modelDict['time'].upper().find(searchTerms[index])
				if found >= 0 :
					tempContext = Context()
					tempContext.begin =  'TIME...'
					if found > 0 :
						regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['time'][found-1::-1]).group(0)
						tempContext.begin += regex[::-1]
					tempContext.bold  =  modelDict['time'][found:(found + len(searchTerms[index]))]
					tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['time'][found + len(searchTerms[index]): found + 100]).group(0)
					match.contexts.append(tempContext)
					continue

				found = modelDict['common']['Summary'].upper().find(searchTerms[index])
				if found >= 0 :
					tempContext = Context()
					tempContext.begin =  'DATE...'
					if found > 0 :
						regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['common']['Summary'][found-1::-1]).group(0)
						tempContext.begin += regex[::-1]
					tempContext.bold  =  modelDict['common']['Summary'][found:(found + len(searchTerms[index]))]
					tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", modelDict['common']['Summary'][found + len(searchTerms[index]): found + 100]).group(0)
					match.contexts.append(tempContext)
					continue

		liDict = getLi(match.idref)
		for index in xrange(numTerms) :
			if matchFound[match.idref][index] == False :
				continue

			found = liDict['floating_text'][index].upper().find(searchTerms[index])
			if found >= 0 :
				tempContext = Context()
				tempContext.begin = liDict['kind'][index] + '...'
				if found > 0 :
					regex = re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", liDict['floating_text'][index][found-1::-1]).group(0)
					#print "SUBSTRING: ", liDict['floating_text'][index][found-1::-1]
					#print "BEFORE CONCATENATION: ", regex
					tempContext.begin += regex[::-1]
					#print "TESTING: ", tempContext.begin
				tempContext.bold  =  liDict['floating_text'][index][found:(found + len(searchTerms[index]))]
				tempContext.end   += re.search("[^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]*", liDict['floating_text'][index][found + len(searchTerms[index]): found + 100]).group(0)
				match.contexts.append(tempContext)
				continue

		# iterate through Li:

class Match() :
	def __init__(self, idref, count) :
		self.idref = idref 
		self.count = count
		self.contexts = []

	def getModel(idref) :
		if idref[0:3] == "CRI" :
			return {"model" : getCrisis(idref), "li": getLi(idref)}
		if idref[0:3] == "PER" :
			return {"model" : getPerson(idref), "li": getLi(idref)}
		if idref[0:3] == "ORG" :
			return {"model" : getOrg(idref), "li": getLi(idref)}

class Context() :
	def __init__(self) :
		self.begin = ''
		self.bold  = ''
		self.end   = ''