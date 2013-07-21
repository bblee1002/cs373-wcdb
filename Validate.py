#!/usr/bin/env python

from lxml import etree
from StringIO import StringIO

xsd = open('WCDB2.xsd.xml', 'r')
xsd = xsd.read()
xsd = StringIO(xsd)
xmlschema_doc = etree.parse(xsd)
xmlschema = etree.XMLSchema(xmlschema_doc)

xml = open('WCDB2.xml', 'r')
xml = xml.read()
xml = StringIO(xml)
xml_doc = etree.parse(xml)
xmlschema.assertValid(xml_doc)
