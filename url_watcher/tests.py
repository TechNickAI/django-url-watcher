from django.http import HttpResponse
from django.test import TestCase
from watcher import create_django_response, check_operator, check_request_rules
from models import Request, RequestRule

class UrlWatcherTest(TestCase):

    def test_operators(self):
        self.assertTrue(check_operator(self.text, 'contains', "Teletubbies"), "contains true") 
        self.assertFalse(check_operator(self.text, 'contains', "not there"), "contains False") 
        self.assertTrue(check_operator(self.text, '!contains', "not there"), "!contains true") 
        self.assertFalse(check_operator(self.text, '!contains', "Teletubbies"), "!contains false") 
        self.assertRaises(Exception, check_operator, self.text, 'unknown operator', 'footext')

    def test_create_django_response(self):
        response = create_django_response("/foo")
        self.assertEqual(response.status_code, 404, "status code on create_django_response")
        self.assertTrue("File not found" in response.content, "content on create_django_response")

    def test_requests(self):
        request = Request(path = "/foo")
        request.save()
        django_response = HttpResponse(self.text)

        # No rules, should pass
        self.assertEqual(len(check_request_rules(request, django_response)), 0)

        # Should have one error now that the status is not 200
        django_response.status_code = 442
        self.assertEqual(len(check_request_rules(request, django_response)), 1)
        
        # set it back for the rest of the tests
        django_response.status_code = 200
        self.assertEqual(len(check_request_rules(request, django_response)), 0)

        rule1 = RequestRule(request = request, target = "content", operator = "contains", value = "Teletubbies")
        rule1.save()
        self.assertEqual(len(check_request_rules(request, django_response)), 0)

        # add a rule that fails
        rule2 = RequestRule(request = request, target = "content", operator = "!contains", value = "Teletubbies")
        rule2.save()
        self.assertEqual(len(check_request_rules(request, django_response)), 1)


        # Done testing requests, now test functionality on the models that have been created
        # str the request to test the __unicode__ method
        str(request) 

        # Test the display_operator
        self.assertEqual(rule2.display_operator, "does not contain")
        rule2.operator='foo'
        # Should not fail on unrecognized operator
        self.assertEqual(rule2.display_operator, "foo")


    # TODO: Test the django management command.
        
    # http://slipsum.com
    text = """Do you see any Teletubbies in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with a blank expression on his face sitting outside on a mechanical helicopter that shakes when you put quarters in it? No? Well, that's what you see at a toy store. And you must think you're in a toy store, because you're here shopping for an infant named Jeb."""
