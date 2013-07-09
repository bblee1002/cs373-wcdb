import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common, list_add


#Embed crises, orgs, and ppl roots within <WC>
def embed_wc (sub_string) :
	#wc_xml.append(sub_string)


#Embed model info under crises, orgs, and ppl
def embed_info (django_models) :
	xml_string = ""
	#Unload info from models into XML
	for d_model in django_models :
		#***diff syntax needed here to work (logic holds for now)
		if d_model == "Crisis" :
			#handle crisis model info
			x_string = "<Crisis ID=" + d_model.crisis_ID + " Name=" d_model.name + ">"
			xml_string.append(x_string)
		if d_model == "Person" :
			#handle person model info
			x_string = "<Person ID=" + d_model.person_ID + " Name=" d_model.name + ">"
			xml_string.append(x_string)
		if d_model == "Org" :
			#handle org model info
			x_string = "<Organization ID=" + d_model.org_ID + " Name=" d_model.name + ">"
			xml_string.append(x_string)




#case: no import happened to fill these models

#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
def receive_import(model_dict) :
	#steps through major categories
	for lkey in model_dict.keys() :
		#Pass root and list of root's models
		embed_info(model_dict[lkey])


