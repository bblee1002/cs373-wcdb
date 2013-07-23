import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common
from getDbModel import  *


def clean_xml (dirty) :
	"""
	Check for presence of "&" invalid XML char in everything but Li() instances.
	Returns a new string w/out any tag information
	"""
	if dirty is None:
		return ''
	return dirty.replace('&', '&amp;')

def make_non_li_string(clean_string, tag):
	return "	<" + tag + ">" + clean_string + "</" + tag + ">\n"

def make_li_string(li_list, tag, coming_from_common = False):
	if len(li_list) == 0:
		return ''
	item_string = ''
	if coming_from_common:
		item_string += "	"
	item_string += 	"	<" + tag + ">\n"
	for item in li_list:
		if coming_from_common:
			item_string += "	"
		item_string = ''.join([item_string,"		<li"])
		if item.href != u'':
			href = clean_xml(item.href)
			item_string = ''.join([item_string," href=\"" + href + "\""])

		if item.embed != u'':
			embed = clean_xml(item.embed)
			item_string = ''.join([item_string," embed=\"" + embed + "\""])

		if item.text != u'':
			text = clean_xml(item.text)
			item_string = ''.join([item_string, " text=\"" + text + "\""])
		item_string = ''.join([item_string, ">"])

		if item.floating_text != u'':
			floating_text = clean_xml(item.floating_text)
			item_string = ''.join([item_string, floating_text])
		item_string = ''.join([item_string, "</li>\n"])
	if not coming_from_common:
		item_string = ''.join([item_string, "	</" + tag + ">\n"])
	else:
		item_string = ''.join([item_string, "		</" + tag + ">\n"])
	return item_string


def make_common_string(common_dict):
	strings = []
	strings.append("	<Common>\n")
	strings.append(make_li_string(common_dict["Citations"], "Citations", True))
	strings.append(make_li_string(common_dict["ExternalLinks"], "ExternalLinks", True))
	strings.append(make_li_string(common_dict["Images"], "Images", True))
	strings.append(make_li_string(common_dict["Videos"], "Videos", True))
	strings.append(make_li_string(common_dict["Maps"], "Maps", True))
	strings.append(make_li_string(common_dict["Feeds"], "Feeds", True))
	if common_dict["Summary"] != u'':
		strings.append("		<Summary>")
		strings.append(common_dict["Summary"])
		strings.append("</Summary>\n")
	strings.append("	</Common>\n")
	if strings == ["	<Common>\n", "", "", "", "", "", "", "	</Common>\n"]:
		return ""
	return ''.join(strings)



#-----Export CRISIS models-----#
def export_crisis (crisis_dict, crisis_id) :
	"""
	Export CRISIS models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	"""
	#assumes all crises have an id and name

	#Start indiv crisis xml string
	strings = []
	strings.append("<Crisis ID=\"" + crisis_id + "\" Name=\"" + str(crisis_dict["name"])+ "\">\n")

	#if there are people listed
	if crisis_dict["people"]        != [] :
		strings.append("	<People>\n")
		for person in crisis_dict["people"] :
			clean_person = clean_xml(str(person[0]))
			strings.append("		<Person ID=\"" + clean_person + "\" />\n")
		strings.append("	</People>\n")
	
	#if there are orgs listed
	if crisis_dict["organizations"] != [] :
		strings.append("	<Organizations>\n")
		for org in crisis_dict["organizations"] :
			clean_org = clean_xml(str(org[0]))
			strings.append("		<Org ID=\"" + clean_org + "\" />\n")
		strings.append("	</Organizations>\n")

	try:
		if crisis_dict["kind"] != '' and crisis_dict["kind"] is not None:
			strings.append(make_non_li_string(clean_xml(str(crisis_dict["kind"])), "Kind"))
	except:
		pass
	try:
		if crisis_dict["date"] != '' and crisis_dict["date"] is not None:
			strings.append(make_non_li_string(clean_xml(str(crisis_dict["date"])), "Date"))
	except:
		pass
	try:
		if crisis_dict["time"] != '' and crisis_dict["time"] is not None:
			strings.append(make_non_li_string(clean_xml(str(crisis_dict["time"])), "Time"))
	except:
		pass
	li_dict = crisis_dict["common"]
	strings.append(make_li_string(li_dict["Locations"], "Locations"))
	strings.append(make_li_string(li_dict["HumanImpact"], "HumanImpact"))
	strings.append(make_li_string(li_dict["EconomicImpact"], "EconomicImpact"))
	strings.append(make_li_string(li_dict["ResourcesNeeded"], "ResourcesNeeded"))
	strings.append(make_li_string(li_dict["WaysToHelp"], "WaysToHelp"))

	strings.append(make_common_string(li_dict))
	
	strings.append("</Crisis>\n\n")
	return ''.join(strings)

#-----Export PERSON models-----#
def export_person (person_dict, person_id) :
	"""
	Export Person models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	""" 

	strings = []
	strings.append("<Person ID=\"" + person_id +  "\" Name=\"" + str(person_dict["name"]) + "\">\n")

	if person_dict["crises"] != [] :
		strings.append("	<Crises>\n")
		for crisis in person_dict["crises"] :
			clean_crisis = clean_xml(str(crisis[0]))
			strings.append("		<Crisis ID=\"" + clean_crisis + "\" />\n")
		strings.append("	</Crises>\n")

	if person_dict["organizations"] != [] :
		strings.append("	<Organizations>\n")
		for org in person_dict["organizations"] :
			clean_org = clean_xml(str(org[0]))
			strings.append("		<Org ID=\"" + clean_org + "\" />\n")
		strings.append("	</Organizations>\n")

	try:
		if person_dict["kind"] != '' and person_dict["kind"] is not None:
			strings.append(make_non_li_string(clean_xml(str(person_dict["kind"])), "Kind"))
	except:
		pass
	try:
		if person_dict["location"] != '' and person_dict["location"] is not None:
			strings.append(make_non_li_string(clean_xml(str(person_dict["location"])), "Location"))
	except:
		pass

	strings.append(make_common_string(person_dict["common"]))
	strings.append("</Person>\n\n")
	return ''.join(strings)

#-----Export ORGANIZATIONS models-----#
def export_organization (org_dict, org_id) :
	"""
	Export Org models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	"""

	strings = []
	strings.append("<Organization ID=\"" + org_id + "\" Name=\"" + str(org_dict["name"]) + "\">\n")

	if org_dict["crises"] != [] :
		strings.append("	<Crises>\n")
		for crisis in org_dict["crises"] :
			clean_crisis = clean_xml(str(crisis[0]))
			strings.append("		<Crisis ID=\"" + clean_crisis + "\" />\n")
		strings.append("	</Crises>\n")

	#if there are people listed
	if org_dict["people"]        != [] :
		strings.append("	<People>\n")
		for person in org_dict["people"] :
			clean_person = clean_xml(str(person[0]))
			strings.append("		<Person ID=\"" + clean_person + "\" />\n")
		strings.append("	</People>\n")

	try:
		if org_dict["time"] != '' and org_dict["time"] is not None:
			strings.append(make_non_li_string(clean_xml(str(org_dict["kind"])), "Kind"))
	except:
		pass
	try:
		if org_dict["location"] != '' and org_dict["location"] is not None:
			strings.append(make_non_li_string(clean_xml(str(org_dict["location"])), "Location"))
	except:
		pass
	
	li_dict = org_dict["common"]
	strings.append(make_li_string(li_dict["History"], "History"))
	strings.append(make_li_string(li_dict["ContactInfo"], "ContactInfo"))	

	strings.append(make_common_string(li_dict))
	strings.append("</Organization>\n\n")
	return ''.join(strings)

#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
#Called from from views.py
def export_xml() :
	"""
	Exports models into an xml string.
	"""

	crisis_ids = getCrisisIDs()
	org_ids = getOrgIDs()
	person_ids = getPeopleIDs()

	crises_xml_string = ["<WorldCrises>\n"]
	for crisis_id in crisis_ids.keys():
		crisis_dict = getCrisis(crisis_id)
		crises_xml_string.append(export_crisis(crisis_dict, crisis_id))

	for person_id in person_ids.keys():
		person_dict = getPerson(person_id)
		crises_xml_string.append(export_person(person_dict, person_id))

	for org_id in org_ids.keys():
		org_dict = getOrg(org_id)
		crises_xml_string.append(export_organization(org_dict, org_id))

	crises_xml_string.append("</WorldCrises>")
	f = open('WCDBExportXML.xml', 'w')
	exportstring = ''.join(crises_xml_string)
	f.write(exportstring.encode('utf8'))
	return exportstring

