"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Crisis, Person, Org, Place


class ModelsCrisisTest(TestCase):
    def test_add_person_1(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        temp        = Crisis()
        test_person = "person"
        temp.add_person(test_person)
        self.assertEqual(temp.person_list[0], "person")
