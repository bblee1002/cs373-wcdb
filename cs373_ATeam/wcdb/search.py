from models import *
from getDbModel import *
from django.db.models import Q

def search(query):
	searchTerms = query.split()

	numTerms = len(searchTerms)

	crises = set()
	people = set()
	orgs = set()


	'''
	# and case
	for term in searchTerms:
		crises = Crisis.objects.filter(Q(crisis_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(date__iregex = term) | Q(time__iregex = term) | Q(common_summary__iregex = term))
		people = Person.objects.filter(Q(person_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term))
		orgs = Org.objects.filter(Q(org_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term))
	'''



	# or case
	for term in searchTerms:
		crises = crises.union(Crisis.objects.filter(Q(crisis_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(date__iregex = term) | Q(time__iregex = term) | Q(common_summary__iregex = term)))
		people = people.union(Person.objects.filter(Q(person_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))
		orgs = orgs.union(Org.objects.filter(Q(org_ID__iregex = term) | Q(name__iregex = term) | Q(kind__iregex = term) | Q(location__iregex = term) | Q(common_summary__iregex = term)))


	matches = set()
	matches = crises.union(people)
	matches = matches.union(orgs)
	return matches


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
