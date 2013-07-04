import os
os.environ["DJANGO_SETTINGS_MODULE"] = "cs373_ATeam.settings"
import sys
from django.conf import settings
from cs373_ATeam.wcdb.models import Crisis
import xml.etree.ElementTree as ET


#Read XML file
strXML = ""
for line in sys.stdin:
		strXML += line

root = ET.fromstring(strXML)
crisis_list = []
#Find instances of crises
#and add to a list of crisis objects created by Django
for node in root.iter("Crisis"):
	temp_crisis = Crisis()
	temp_crisis.crisis_ID = node.get("ID")
	temp_crisis.name= node.get("Name")
	crisis_list.append(temp_crisis)

for crisis in crisis_list:
	print "crisis id: ", crisis.crisis_ID, "crisis name: ", crisis.name

