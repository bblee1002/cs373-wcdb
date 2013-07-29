from models import *

def search(query):
	searchTerms = query.split()

	numTerms = len(searchTerms)


	crises = []
	people = []
	orgs = []

	matches = set()

	crises += Crisis.objects.filter(name__iregex = query)
	for i in crises:
		matches.add(match(i.crisis_ID))

	people += Person.objects.filter(name__iregex = query)
	for i in people:
		matches.add(match(i.crisis_ID))

	orgs += Org.objects.filter(name__iregex = query)
	for i in crises:
		matches.add(match(i.crisis_ID))

	orset = set()

	for term in searchTerms:
		crises = Crisis.objects.filter(name__iregex = term)
		countIncrement(crises, orObjects)
		people = Person.objects.filter(name__iregex = term)
		countIncrement(people, orObjects)
		orgs = Org.objects.filter(name__iregex = term)
		countIncrement(orgs, orObjects)

	


	matches += orset


	for x in matches:
		print x.name

	return matches


def countIncrement(container, orObjects):
	found = False
	for object in orObjects:
		for match in matches:
			if object == match:
				object.count += 1
				found = True
		if !found:
			matches.add(i)



class match():
	def __init__(self, id):
		self.id = id
		self.context
		self.count
