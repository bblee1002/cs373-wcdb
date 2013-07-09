"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Crisis, Person, Org


class ModelsCrisisTest(TestCase):

	#---------------------------------------#
	#-----Unit Tests for functions from models.py
	#---------------------------------------#


    def test_list_add(self):
        """
        Tests .
        """
        temp        = Crisis()
        person = "random_person"
        list_add(temp.people, person)
        self.assertEqual(temp.people[0], "random_person")

	def test_li_populate(self):
		temp = Element()
		temp.set("href", "href_stuff")
		temp.text = "randomfloatingtext"
		temp_li = Li()
		temp_li.populate(temp)
		self.assertEqual(temp_li.href == "href_stuff")

	def test_common_populate(self):
		temp_com = Common()
		xml_string = "<Common><Citations><li>The Hindustan Times</li></Citations><ExternalLinks><li href="http://en.wikipedia.org/wiki/2013_North_India_floods">Wikipedia</li></ExternalLinks><Images><li embed="http://timesofindia.indiatimes.com/photo/15357310.cms" /></Images><Videos><li embed="//www.youtube.com/embed/qV3s7Sa6B6w" /></Videos><Maps><li embed="https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed" /></Maps><Feeds><li embed="[WHATEVER A FEED URL LOOKS LIKE]" /></Feeds><Summary>Lorem ipsum...</Summary></Common>"
		root = ET.fromstring(xml_string)
		temp_com.populate(root)

		self.assertEqual(temp_com.citations[0] == "The Hindustan Times")
		self.assertEqual(temp_com.external_links[0] == "http://en.wikipedia.org/wiki/2013_North_India_floods")
		self.assertEqual(temp_com.images[0] == "http://timesofindia.indiatimes.com/photo/15357310.cms")
		self.assertEqual(temp_com.videos[0] == "//www.youtube.com/embed/qV3s7Sa6B6w")
		self.assertEqual(temp_com.maps[0] == "https://www.google.com/maps?sll=30.08236989592049,79.31189246107706&amp;sspn=3.2522150867582833,7.2072687770004205&amp;t=m&amp;q=uttarakhand&amp;dg=opt&amp;ie=UTF8&amp;hq=&amp;hnear=Uttarakhand,+India&amp;ll=30.066753,79.0193&amp;spn=2.77128,5.07019&amp;z=8&amp;output=embed")
		self.assertEqual(temp_com.feeds[0] == "[WHATEVER A FEED URL LOOKS LIKE]")
		self.assertEqual(temp_com.videos[0] == "Lorem ipsum...")
		



