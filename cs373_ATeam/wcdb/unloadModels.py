import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common



#Check for presence of "&" invalid XML char
#in everything but Li() instances
#Returns a new string w/out any tag information
def clean_xml (dirty) :	
	dirty_clean = dirty.split("&")
	for dirty_piece in dirty_clean:
		#first element case
		if dirty_piece == dirty_clean[0] :
			dirty_new = dirty_piece
		else :
			dirty_new += "&amp;" + dirty_piece
	return dirty_new


#-----Export CRISIS models-----#
def export_crisis (crisis) :
	#assumes all crises have an id and name
	assert crisis.crisis_ID != None
	assert crisis.name != None

	#Start indiv crisis xml string
	crisis_string = "<Crisis ID=\"" + crisis.crisis_ID + "\" Name=\"" + crisis.name + "\">"
	
	#if there are people listed
	if crisis.people        != [] :
		p_string = "<People>"
		for person in crisis.people :
			clean_person = clean_xml(person)
			p_string += "<Person ID=\"" + clean_person + "\" />"
		p_string +="</People>"
		crisis_string += p_string
	
	#if there are orgs listed
	if crisis.organizations != [] :
		o_string = "<Organizations>"
		for org in crisis.organizations :
			clean_org = clean_xml(org)
			o_string += "<Org ID=\"" + clean_org + "\" />"
		o_string += "</Organizations>"
		crisis_string += o_string

	if crisis.kind is not None :
		clean_k = clean_xml(crisis.kind)
		k = "<Kind>" + clean_k + "</Kind>"
		crisis_string += k
	if crisis.date is not None :
		clean_d = clean_xml(crisis.date)
		d = "<Date>" + clean_d + "</Date>"
		crisis_string += d
	if crisis.time is not None :
		clean_t = clean_xml(crisis.time)
		t = "<Time>" + clean_t + "</Time>"
		crisis_string += t
		

	#handle li lists
	if crisis.locations        != [] :
		root = "Locations"
		xml_locations = crisis.common.xml_from_li(root, crisis.locations)
		crisis_string += xml_locations
	if crisis.human_impact     != [] :
		root = "HumanImpact"
		xml_human_impact = crisis.common.xml_from_li(root, crisis.human_impact)
		crisis_string += xml_human_impact
	if crisis.economic_impact  != [] :
		root = "EconomicImpact"
		xml_economic_impact = crisis.common.xml_from_li(root, crisis.economic_impact)
		crisis_string += xml_economic_impact
	if crisis.resources_needed != [] :
		root = "ResourcesNeeded"
		xml_resources_needed = crisis.common.xml_from_li(root, crisis.resources_needed)
		crisis_string += xml_resources_needed
	if crisis.ways_to_help     != [] :
		root = "WaysToHelp"
		xml_ways_to_help = crisis.common.xml_from_li(root, crisis.ways_to_help)
		crisis_string += xml_ways_to_help

	#Export info from the common class
	if crisis.common is not None :
		crisis_string += crisis.common.print_xml()

	#Conclude crisis xml
	crisis_string += "</Crisis>"
	return crisis_string



#-----Export PERSON models-----#
def export_person (person) :
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
def receive_import(model_dict) :

	#collect xml versions of all CRISIS models
	crises_xml_string = ""
	for crisis in model_dict["crises"] :
		crises_xml_string += export_crisis (crisis)

	#collect xml versions of all PERSON models
	people_xml_string = ""
	for person in model_dict["people"] :
		people_xml_string += export_person (person)

	#collect xml versions of all ORGANIZATION models
	organizations_xml_string = ""
	for org in model_dict["organizations"] :
		organizations_xml_string += export_organization (org)

	return "<WorldCrises>" + crises_xml_string + people_xml_string + organizations_xml_string + "</WorldCrises>"



