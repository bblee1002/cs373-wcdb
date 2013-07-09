import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common, list_add


#Embed crises, orgs, and ppl roots within <WC>
def embed_wc (sub_string) :
	#wc_xml.append(sub_string)



#case: no import happened to fill these models

#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
def receive_import(model_dict) :
	#export crises models
	for crisis in filled_models["crises"] :
		#assumes all crises have an id and name
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
		#if there are locations listed
		if crisis.locations != [] :
        	l_string = "<Locations>"
        	for loc in crisis.locations :
        		l_string.append("<li>" + loc + "</li>")
    		l_string.append("</Locations>")
		#if there are impacts listed
		if crisis.human_impact != [] :
        	h_string = "<HumanImpact>"
        	for hi in crisis.human_impact :
        		h_string.append("<li>" + hi + "</li>")
    		h_string.append("</HumanImpact>")
		#if there are human impacts listed
		if crisis.human_impact != [] :
        	h_string = "<HumanImpact>"
        	for hi in crisis.human_impact :
        		h_string.append("<li>" + hi + "</li>")
    		h_string.append("</HumanImpact>")
		#if there are economic impacts listed
		if crisis.economic_impact != [] :
        	e_string = "<EconomicImpact>"
        	for ei in crisis.human_impact :
        		e_string.append("<li>" + ei + "</li>")
    		e_string.append("</EconomicImpact>")
		#if there are resources listed
		if crisis.resources_needed != [] :
        	r_string = "<ResourcesNeeded>"
        	for rn in crisis.resources_needed :
        		r_string.append("<li>" + rn + "</li>")
    		e_string.append("</ResourcesNeeded>")
		#if there are ways to help
		if crisis.ways_to_help != [] :
        	w_string = "<WaysToHelp>"
        	for wth in crisis.ways_to_help :
        		r_string.append("<li>" + wth + "</li>")
    		e_string.append("</WaysToHelp>")
        
