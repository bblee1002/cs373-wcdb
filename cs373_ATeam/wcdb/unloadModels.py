import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common, list_add


#Embed crises, orgs, and ppl roots within <WC>
#def embed_wc (sub_string) :
	#wc_xml.append(sub_string)

def xml_from_li_list(root_str, model_list) :
	xml_string = "<" + root_str ">"
	for li in model_list :
		xml_string.append("<li>" + li + "</li>")
	xml_string.append("</" + root_str ">")


#case: no import happened to fill these models

#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
def receive_import(model_dict) :
	#export crises models
	for crisis in filled_models["crises"] :
		#assumes all crises have an id and name
		assert crisis.crisis_ID != None
		assert crisis.name != None
        crisis_string = "<Crisis ID=\"" + crisis.crisis_ID + "\" Name=\"" + crisis.name + "\">"
        #if there are people listed
        if crisis.people != [] :
        	p_string = "<People>"
        	for person in crisis.people :
        		p_string.append("<Person ID=\"" + person.person_ID + "\" />")
    		p_string.append("</People>")
		#if there are orgs listed
		if crisis.organizations != [] :
        	o_string = "<Organizations>"
        	for org in crisis.organizations :
        		o_string.append("<Org ID=\"" + org.org_ID + "\" />")
    		o_string.append("</Organizations>")
		if crisis.kind is not None :
			k = "<Kind>" + crisis.kind + "</Kind>"
		if crisis.date is not None :
			d = "<Date>" + crisis.date + "</Date>"
		if crisis.time is not None :
			d = "<Time>" + crisis.time + "</Time>"

		#handle li lists of models
		if crisis.locations != [] :
        	root = "Locations"
        	xml_from_li_list(root, crisis.locations)
        	
		if crisis.human_impact != [] :
        	root = "HumanImpact"
        	xml_from_li_list(root, crisis.human_impact)


		if crisis.economic_impact != [] :
        	root = "EconomicImpact"
        	xml_from_li_list(root, crisis.economic_impact)

		#if there are resources listed
		if crisis.resources_needed != [] :
        	root = "ResourcesNeeded"
        	xml_from_li_list(root, crisis.resources_needed)

		#if there are ways to help
		if crisis.ways_to_help != [] :
        	root = "WaysToHelp"
        	xml_from_li_list(root, crisis.ways_to_help)
		#export 
        
