from lxml import etree
from StringIO import StringIO

xsd = open('WorldCrises.xsd.xml', 'r')
xsd = xsd.read()
xsd = StringIO(xsd)
xmlschema_doc = etree.parse(xsd)
xmlschema = etree.XMLSchema(xmlschema_doc)

xml = open('WorldCrises.xml', 'r')
xml = xml.read()
xml = StringIO(xml)
xml_doc = etree.parse(xml)
xmlschema.assertValid(xml_doc)
