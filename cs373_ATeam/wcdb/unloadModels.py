import sys
import xml.etree.ElementTree as ET
from models import Crisis, Person, Org, Li, Common, list_add


#Embed crises, orgs, and ppl roots within <WC>
#def embed_wc (sub_string) :
	#wc_xml.append(sub_string)

#Return xml string rep nested list items beneath root
def xml_from_li_list(root_str, model_list) :
	xml_string = "<" + root_str + ">"
	for li in model_list :
		xml_string.append("<li>" + li + "</li>")
	xml_string.append("</" + root_str + ">")
	return xml_string


#case2handle: no import happened to fill these models

#Access models thrgh arg model_dict = {Crises : [], Orgs : [], Ppl : []}
def receive_import(model_dict) :

	#------------------------------#
	#-----Export crises models-----#
	crises_xml_string = ""

	for crisis in filled_models["crises"] :

		#assumes all crises have an id and name
		assert crisis.crisis_ID != None
		assert crisis.name != None

		#Start indiv crisis xml string
		crisis_string = "<Crisis ID=\"" + crisis.crisis_ID + "\" Name=\"" + crisis.name + "\">"
		#if there are people listed
		if crisis.people        != [] :
			p_string = "<People>"
			for person in crisis.people :
				p_string.append("<Person ID=\"" + person + "\" />")
			p_string.append("</People>")
			#ADD to current crisis xml string
			crisis_string.append(p_string)
		
		#if there are orgs listed
		if crisis.organizations != [] :
			o_string = "<Organizations>"
			for org in crisis.organizations :
				o_string.append("<Org ID=\"" + org + "\" />")
			o_string.append("</Organizations>")
			#ADD to current crisis xml string
			crisis_string.append(o_string)

		if crisis.kind is not None :
			k = "<Kind>" + crisis.kind + "</Kind>"
			#ADD to current crisis xml string
			crisis_string.append(k)
		if crisis.date is not None :
			d = "<Date>" + crisis.date + "</Date>"
			#ADD to current crisis xml string
			crisis_string.append(d)
		if crisis.time is not None :
			t = "<Time>" + crisis.time + "</Time>"
			#ADD to current crisis xml string
			crisis_string.append(t)
			

		#handle li lists of models
		if crisis.locations        != [] :
			root = "Locations"
			xml_locations = xml_from_li_list(root, crisis.locations)
			#ADD to current crisis xml string
			crisis_string.append(xml_locations)  	
		if crisis.human_impact     != [] :
			root = "HumanImpact"
			xml_human_impact = xml_from_li_list(root, crisis.human_impact)
			#ADD to current crisis xml string
			crisis_string.append(xml_human_impact)
		if crisis.economic_impact  != [] :
			root = "EconomicImpact"
			xml_economic_impact = xml_from_li_list(root, crisis.economic_impact)
			#ADD to current crisis xml string
			crisis_string.append(xml_economic_impact)
		if crisis.resources_needed != [] :
			root = "ResourcesNeeded"
			xml_resources_needed = xml_from_li_list(root, crisis.resources_needed)
			#ADD to current crisis xml string
			crisis_string.append(xml_resources_needed)
		if crisis.ways_to_help     != [] :
			root = "WaysToHelp"
			xml_ways_to_help = xml_from_li_list(root, crisis.ways_to_help)
			#ADD to current crisis xml string
			crisis_string.append(xml_ways_to_help)

		#Export info from the common class
		if crisis.common is not None:
			crisis_string.append("<Common>")
			if crisis.common.citations != [] :
				root = "Citations"
				xml_citations = xml_from_li_list(root, crisis.common.citations)
				#ADD to current crisis xml string
				crisis_string.append(xml_citations)
			if crisis.external_links   != [] :
				root = "ExternalLinks"
				xml_external_links = xml_from_li_list(root, crisis.common.external_links)
				#ADD to current crisis xml string
				crisis_string.append(xml_external_links)
			if crisis.common.images    != [] :
				root = "Images"
				xml_images = xml_from_li_list(root, crisis.common.images)
				#ADD to current crisis xml string
				crisis_string.append(xml_images)
			if crisis.common.videos    != [] :
				root = "Videos"
				xml_videos = xml_from_li_list(root, crisis.common.videos)
				#ADD to current crisis xml string
				crisis_string.append(xml_videos)
			if crisis.common.maps      != [] :
				root = "Maps"
				xml_maps = xml_from_li_list(root, crisis.common.maps)
				#ADD to current crisis xml string
				crisis_string.append(xml_maps)
			if crisis.common.feeds     != [] :
				root = "Feeds"
				xml_feeds = xml_from_li_list(root, crisis.common.feeds)
				#ADD to current crisis xml string
				crisis_string.append(xml_feeds)
				if crisis.common.summary is not None:
				#ADD to current crisis xml string
				crisis_string.append("<Summary>" + crisis.common.summary + "</Summary" )
			crisis_string.append("</Common>")

		#Conclude crisis xml and concat to crises_xml_string
		crisis_string.append("</Crisis>")
		crises_xml_string.append(crisis_string)




