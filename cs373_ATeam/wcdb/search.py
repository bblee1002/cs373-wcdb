from models import *

def search(query):
	searchTerms = query.split()

	numTerms = len(searchTerms)


	crises = []
	people = []
	orgs = []

	matches = []
	matches += Crisis.objects.filter(name__iregex = query)
	matches += Person.objects.filter(name__iregex = query)
	matches += Org.objects.filter(name__iregex = query)

	orObjects = []

	for term in searchTerms:
		orObjects += Crisis.objects.filter(name__iregex = term)
		orObjects += Person.objects.filter(name__iregex = term)
		orObjects += Org.objects.filter(name__iregex = term)

	orset = set(orObjects)


	matches += orset


	for x in matches:
		print x.name

	return matches



class match():
	def __init__(self, id):
		self.id = id
		self.context
		self.count
