from models import *
from getDbModel import *

def search(query):
	searchTerms = query.split()

	numTerms = len(searchTerms)

	crises = Crisis.objects.all()
	people = Person.objects.all()
	orgs = Org.objects.all()

	for crisis in crises:



	# or case
	for term in searchTerms:
		crises = Crisis.objects.filter(crisis_ID__iregex = term or name__iregex = term or kind__iregex = term or date__iregex = term or time__iregex = term or common_summary__iregex = term)
		people = Person.objects.filter(person_ID__iregex = term or name__iregex = term or kind__iregex = term or location__iregex = term or common_summary__iregex = term)
		orgs = Org.objects.filter(org_ID__iregex = term or name__iregex = term or kind__iregex = term or location__iregex = term or common_summary__iregex = term)



'''
	crises = []
	people = []
	orgs = []

	matches = set()

	# exact match
	crises += Crisis.objects.filter(name__iregex = query)
	for i in crises:
		matches.add(match(i.crisis_ID))

	people += Person.objects.filter(name__iregex = query)
	for i in people:
		matches.add(match(i.crisis_ID))

	orgs += Org.objects.filter(name__iregex = query)
	for i in crises:
		matches.add(match(i.crisis_ID))

	# and case
	for term in searchTerms:
		crises = Crisis.objects.filter(name__iregex = term)
		countIncrement(crises, orObjects)
		people = Person.objects.filter(name__iregex = term)
		countIncrement(people, orObjects)
		orgs = Org.objects.filter(name__iregex = term)
		countIncrement(orgs, orObjects)


	orset = set()
	


	matches += orset


	for x in matches:
		print x.name

	return matches
'''

def countIncrement(container, orObjects):
	found = False
	for object in orObjects:
		for match in matches:
			if object == match:
				object.count += 1
				found = True
		if not found:
			matches.add(i)



class match():
	def __init__(self, id):
		self.id = id
		self.context
		self.count
