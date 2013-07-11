import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common, list_add




#-----Return xml string rep nested list items beneath root-----#
def xml_from_li_list(root_str, model_list) :
	xml_string = "<" + root_str + ">"
	for li in model_list :
		xml_string += "<li>" + str(li) + "</li>"
	xml_string += "</" + root_str + ">"
	return xml_string



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
			p_string += "<Person ID=\"" + person + "\" />"
		p_string +="</People>"
		#ADD to current crisis xml string
		crisis_string += p_string
	
	#if there are orgs listed
	if crisis.organizations != [] :
		o_string = "<Organizations>"
		for org in crisis.organizations :
			o_string += "<Org ID=\"" + org + "\" />"
		o_string += "</Organizations>"
		#ADD to current crisis xml string
		crisis_string += o_string

	if crisis.kind is not None :
		k = "<Kind>" + crisis.kind + "</Kind>"
		#ADD to current crisis xml string
		crisis_string += k
	if crisis.date is not None :
		d = "<Date>" + crisis.date + "</Date>"
		#ADD to current crisis xml string
		crisis_string += d
	if crisis.time is not None :
		t = "<Time>" + crisis.time + "</Time>"
		#ADD to current crisis xml string
		crisis_string += t
		

	#handle li lists of models
	if crisis.locations        != [] :
		root = "Locations"
		xml_locations = xml_from_li_list(root, crisis.locations)
		#ADD to current crisis xml string
		crisis_string += xml_locations
	if crisis.human_impact     != [] :
		root = "HumanImpact"
		xml_human_impact = xml_from_li_list(root, crisis.human_impact)
		#ADD to current crisis xml string
		crisis_string += xml_human_impact
	if crisis.economic_impact  != [] :
		root = "EconomicImpact"
		xml_economic_impact = xml_from_li_list(root, crisis.economic_impact)
		#ADD to current crisis xml string
		crisis_string += xml_economic_impact
	if crisis.resources_needed != [] :
		root = "ResourcesNeeded"
		xml_resources_needed = xml_from_li_list(root, crisis.resources_needed)
		#ADD to current crisis xml string
		crisis_string += xml_resources_needed
	if crisis.ways_to_help     != [] :
		root = "WaysToHelp"
		xml_ways_to_help = xml_from_li_list(root, crisis.ways_to_help)
		#ADD to current crisis xml string
		crisis_string += xml_ways_to_help

	#Export info from the common class
	if crisis.common is not None:
		crisis_string += "<Common>"
		if crisis.common.citations != [] :
			root = "Citations"
			xml_citations = xml_from_li_list(root, crisis.common.citations)
			#ADD to current crisis xml string
			crisis_string += xml_citations
		if crisis.common.external_links   != [] :
			root = "ExternalLinks"
			xml_external_links = xml_from_li_list(root, crisis.common.external_links)
			#ADD to current crisis xml string
			crisis_string += xml_external_links
		if crisis.common.images    != [] :
			root = "Images"
			xml_images = xml_from_li_list(root, crisis.common.images)
			#ADD to current crisis xml string
			crisis_string += xml_images
		if crisis.common.videos    != [] :
			root = "Videos"
			xml_videos = xml_from_li_list(root, crisis.common.videos)
			#ADD to current crisis xml string
			crisis_string += xml_videos
		if crisis.common.maps      != [] :
			root = "Maps"
			xml_maps = xml_from_li_list(root, crisis.common.maps)
			#ADD to current crisis xml string
			crisis_string += xml_maps
		if crisis.common.feeds     != [] :
			root = "Feeds"
			xml_feeds = xml_from_li_list(root, crisis.common.feeds)
			#ADD to current crisis xml string
			crisis_string += xml_feeds
		if crisis.common.summary is not None:
			#ADD to current crisis xml string
			crisis_string += "<Summary>" + crisis.common.summary + "</Summary" 
		crisis_string += "</Common>"

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
			pc_string += "<Crisis ID=\"" + p_crisis + "\" />"
		pc_string +="</Crises>"
		#ADD to current crisis xml string
		person_string += pc_string
	
	#if there are orgs listed
	if person.organizations != [] :
		o_string = "<Organizations>"
		for org in person.organizations :
			o_string += "<Org ID=\"" + org + "\" />"
		o_string += "</Organizations>"
		#ADD to current crisis xml string
		person_string += o_string

	if person.kind is not None :
		k = "<Kind>" + person.kind + "</Kind>"
		#ADD to current crisis xml string
		person_string += k

	if person.location is not None :
		l = "<Location>" + person.location + "</Location>"
		#ADD to current crisis xml string
		person_string += l

	#Export info from the common class
	if person.common is not None:
		person_string += "<Common>"
		if person.common.citations != [] :
			root = "Citations"
			xml_citations = xml_from_li_list(root, person.common.citations)
			#ADD to current person xml string
			person_string += xml_citations
		if person.common.external_links   != [] :
			root = "ExternalLinks"
			xml_external_links = xml_from_li_list(root, person.common.external_links)
			#ADD to current person xml string
			person_string += xml_external_links
		if person.common.images    != [] :
			root = "Images"
			xml_images = xml_from_li_list(root, person.common.images)
			#ADD to current person xml string
			person_string += xml_images
		if person.common.videos    != [] :
			root = "Videos"
			xml_videos = xml_from_li_list(root, person.common.videos)
			#ADD to current person xml string
			person_string += xml_videos
		if person.common.maps      != [] :
			root = "Maps"
			xml_maps = xml_from_li_list(root, person.common.maps)
			#ADD to current person xml string
			person_string += xml_maps
		if person.common.feeds     != [] :
			root = "Feeds"
			xml_feeds = xml_from_li_list(root, person.common.feeds)
			#ADD to current person xml string
			person_string += xml_feeds
		if person.common.summary is not None:
			#ADD to current person xml string
			person_string += "<Summary>" + person.common.summary + "</Summary" 
		person_string += "</Common>"

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
			oc_string += "<Crisis ID=\"" + o_crisis + "\" />"
		oc_string +="</Crises>"
		#ADD to current org xml string
		org_string += oc_string
	
	#if there are people listed
	if org.people != [] :
		op_string = "<Organizations>"
		for org_person in org.people :
			op_string += "<Org ID=\"" + org_person + "\" />"
		op_string += "</Organizations>"
		#ADD to current org xml string
		org_string += op_string

	if org.kind is not None :
		k = "<Kind>" + org.kind + "</Kind>"
		#ADD to current org xml string
		org_string += k

	if org.location is not None :
		l = "<Location>" + org.location + "</Location>"
		#ADD to current org xml string
		org_string += l

	#handle li lists of models
	if org.history        != [] :
		root = "History"
		xml_history = xml_from_li_list(root, org.history)
		#ADD to current org xml string
		org_string += xml_history
	if org.contact     != [] :
		root = "ContactInfo"
		xml_contact = xml_from_li_list(root, org.contact)
		#ADD to current org xml string
		org_string += xml_contact

	#Export info from the common class
	if org.common is not None:
		org_string += "<Common>"
		if org.common.citations != [] :
			root = "Citations"
			xml_citations = xml_from_li_list(root, org.common.citations)
			#ADD to current org xml string
			org_string += xml_citations
		if org.common.external_links   != [] :
			root = "ExternalLinks"
			xml_external_links = xml_from_li_list(root, org.common.external_links)
			#ADD to current org xml string
			org_string += xml_external_links
		if org.common.images    != [] :
			root = "Images"
			xml_images = xml_from_li_list(root, org.common.images)
			#ADD to current org xml string
			org_string += xml_images
		if org.common.videos    != [] :
			root = "Videos"
			xml_videos = xml_from_li_list(root, org.common.videos)
			#ADD to current org xml string
			org_string += xml_videos
		if org.common.maps      != [] :
			root = "Maps"
			xml_maps = xml_from_li_list(root, org.common.maps)
			#ADD to current org xml string
			org_string += xml_maps
		if org.common.feeds     != [] :
			root = "Feeds"
			xml_feeds = xml_from_li_list(root, org.common.feeds)
			#ADD to current org xml string
			org_string += xml_feeds
		if org.common.summary is not None:
			#ADD to current org xml string
			org_string += "<Summary>" + org.common.summary + "</Summary" 
		org_string += "</Common>"

	#Conclude organization xml
	org_string += "</Organization>"
	return org_string


#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
#passed from views.py
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



