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
	return "<" + tag + ">" + clean_string + "</" + tag + ">"

def make_li_string(li_list, tag):
	if len(li_list) == 0:
		return ''
	item_string = "<" + tag + ">"
	for item in li_list:
		item_string.join("<li")
		if item.href != u'':
			href = clean_xml(item.href)
			item_string.join(" href=\"" + href + "\"")

		if item.embed != u'':
			embed = clean_xml(item.embed)
			item_string.join(" embed=\"" + embed + "\"")

		if item.text != u'':
			text = clean_xml(item.text)
			item_string.join(" text=\"" + text + "\"")
		item_string.join(">")

		if item.floating_text != u'':
			floating_text = clean_xml(item.floating_text)
			item_string.join(floating_text)
		item_string.join("</li>")
	item_string.join("</" + tag + ">")
	return item_string


def make_common_string(common_dict):
	common_string = "<Common>"
	make_li_string(common_dict["Citations"], "Citations")
	make_li_string(common_dict["ExternalLinks"], "ExternalLinks")
	make_li_string(common_dict["Images"], "Images")
	make_li_string(common_dict["Videos"], "Videos")
	make_li_string(common_dict["Maps"], "Maps")
	make_li_string(common_dict["Feeds"], "Feeds")
	common_string.join("</Common>")



#-----Export CRISIS models-----#
def export_crisis (crisis_dict, crisis_id) :
	"""
	Export CRISIS models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	"""
	#assumes all crises have an id and name

	#Start indiv crisis xml string
	crisis_string = "<Crisis ID=\"" + crisis_id + "\" Name=\"" + str(crisis_dict["name"])+ "\">"


	#if there are people listed
	if crisis_dict["people"]        != [] :
		p_string = "<People>"
		for person in crisis_dict["people"] :
			clean_person = clean_xml(str(person[0]))
			p_string.join("<Person ID=\"" + clean_person + "\" />")
		p_string.join("</People>")
		crisis_string.join(p_string)
	
	#if there are orgs listed
	if crisis_dict["organizations"] != [] :
		o_string = "<Organizations>"
		for org in crisis.organizations :
			clean_org = clean_xml(str(org[0]))
			o_string.join("<Org ID=\"" + clean_org + "\" />")
		o_string.join("</Organizations>")
		crisis_string.join(o_string)

	try:
		crisis_string.join(make_non_li_string(clean_xml(str(crisis_dict["kind"])), "Kind"))
	except:
		pass
	try:
		crisis_string.join(make_non_li_string(clean_xml(str(crisis_dict["date"])), "Date"))
	except:
		pass
	try:
		crisis_string.join(make_non_li_string(clean_xml(str(crisis_dict["time"])), "Time"))
	except:
		pass
	li_dict = crisis_dict["common"]
	crisis_string.join(make_li_string(li_dict["Locations"], "Locations"))
	crisis_string.join(make_li_string(li_dict["HumanImpact"], "HumanImpact"))
	crisis_string.join(make_li_string(li_dict["EconomicImpact"], "EconomicImpact"))
	crisis_string.join(make_li_string(li_dict["ResourcesNeeded"], "ResourcesNeeded"))
	crisis_string.join(make_li_string(li_dict["WaystoHelp"], "WaysToHelp"))

	crisis_string.join(make_common_string(li_dict))
	crisis_string.join(make_li_string(li_dict["Summary"], "Summary"))

	crisis_string += "</Crisis>"
	return crisis_string



#-----Export PERSON models-----#
def export_person (person) :
	"""
	Export Person models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	"""
	#assumes all people have an id and name
	assert person.person_ID != None
	assert person.name != None

	#Start indiv person xml string
	person_string = "<Person ID=\"" + person.person_ID + "\" Name=\"" + person.name + "\">"
	
	#if there are crises listed
	if person.crises        != [] :
		pc_string = "<Crises>"
		for p_crisis in person.crises :
			clean_person = clean_xml(p_crisis)
			pc_string += "<Crisis ID=\"" + clean_person + "\" />"
		pc_string +="</Crises>"
		person_string += pc_string
	
	#if there are orgs listed
	if person.organizations != [] :
		o_string = "<Organizations>"
		for org in person.organizations :
			clean_org = clean_xml(org)
			o_string += "<Org ID=\"" + clean_org + "\" />"
		o_string += "</Organizations>"
		person_string += o_string

	if person.kind is not None :
		clean_k = clean_xml(person.kind)
		k = "<Kind>" + clean_k + "</Kind>"
		person_string += k

	if person.location is not None :
		clean_l = clean_xml(person.location)
		l = "<Location>" + clean_l + "</Location>"
		person_string += l
	
	#Export info from the common class
	if person.common is not None :
		person_string += person.common.print_xml()

	#Conclude person xml
	person_string += "</Person>"
	return person_string



#-----Export ORGANIZATIONS models-----#
def export_organization (org) :
	"""
	Export Org models by extracting information from the relevant class.
	Builds a string to return at the end as parse elements of crisis.
	"""
	#assumes all orgs have an id and name
	assert org.org_ID != None
	assert org.name != None

	#Start indiv org xml string
	org_string = "<Organization ID=\"" + org.org_ID + "\" Name=\"" + org.name + "\">"
	
	#if there are crises listed
	if org.crises        != [] :
		oc_string = "<Crises>"
		for o_crisis in org.crises :
			clean_crisis = clean_xml(o_crisis)
			oc_string += "<Crisis ID=\"" + clean_crisis + "\" />"
		oc_string +="</Crises>"
		#ADD to current org xml string
		org_string += oc_string
	
	#if there are people listed
	if org.people != [] :
		op_string = "<People>"
		for org_person in org.people :
			clean_person = clean_xml(org_person)
			op_string += "<Person ID=\"" + clean_person + "\" />"
		op_string += "</People>"
		#ADD to current org xml string
		org_string += op_string

	if org.kind is not None :
		clean_k = clean_xml(org.kind)
		k = "<Kind>" + clean_k + "</Kind>"
		#ADD to current org xml string
		org_string += k

	if org.location is not None :
		clean_l = clean_xml(org.location)
		l = "<Location>" + clean_l + "</Location>"
		#ADD to current org xml string
		org_string += l

	#handle li lists of models
	if org.history        != [] :
		root = "History"
		xml_history = org.common.xml_from_li(root, org.history)
		#ADD to current org xml string
		org_string += xml_history
	if org.contact     != [] :
		root = "ContactInfo"
		xml_contact = org.common.xml_from_li(root, org.contact)
		#ADD to current org xml string
		org_string += xml_contact

	#Export info from the common class
	if org.common is not None :
		org_string += org.common.print_xml()

	#Conclude organization xml
	org_string += "</Organization>"
	return org_string


#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
#Called from from views.py
def receive_import() :
	"""
	Exports models into an xml string.
	"""

	crisis_ids = getCrisisIDs()
	org_ids = getOrgIDs()
	person_ids = getPeopleIDs()

	crises_xml_string = ""
	for crisis_id in crisis_ids.keys():
		crisis_dict = getCrisis(crisis_id)
		crises_xml_string.join(export_crisis(crisis_dict, crisis_id))

	for person_id in person_ids.keys():
		person_dict = getPerson(person_id)
		crises_xml_string.join(export_person(person_dict))

	for org_id in org_ids.keys():
		org_dict = getOrg(org_id)
		crises_xml_string.join(export_org(org_dict))

	return "<WorldCrises>" + crises_xml_string + "</WorldCrises>"

