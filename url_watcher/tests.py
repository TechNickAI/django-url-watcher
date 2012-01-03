from django.test import TestCase
from watcher import check_operator, check_request_rules
from models import Request, RequestRules

class UrlWatcherTest(TestCase):

    def test_operators(self):
        self.assertTrue(check_operator(self.text, 'contains', "Teletubbies"), "contains true") 
        self.assertFalse(check_operator(self.text, 'contains', "not there"), "contains False") 
        self.assertTrue(check_operator(self.text, '!contains', "not there"), "!contains true") 
        self.assertFalse(check_operator(self.text, '!contains', "Teletubbies"), "!contains false") 
        self.assertRaises(Exception, self.text, 'unknown operator', 'footext')
        pass 

    # http://slipsum.com
    text = """Do you see any Teletubbies in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with a blank expression on his face sitting outside on a mechanical helicopter that shakes when you put quarters in it? No? Well, that's what you see at a toy store. And you must think you're in a toy store, because you're here shopping for an infant named Jeb."""
