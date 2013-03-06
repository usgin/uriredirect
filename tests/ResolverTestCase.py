from django.test import TestCase
from django.test.client import Client
from uriredirect.views import resolve_uri

class ResolverTestCase(TestCase):
    fixtures = [ 'test_uriregister.json', 'test_rewriterule.json', 'test_mediatype.json', 'test_acceptmapping.json' ]
    
    def setUp(self):
        self.c = Client()
        self.basePath = '/' # this needs to be configured depending on how you've set up URL structure in your Django project
    
    def test_resolve_uri_invalid_HTTP_method(self):
        result = self.c.post(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 405, 'Resolver.resolve_uri did not return a 405 error when receiving a POST')
        
        result = self.c.head(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 405, 'Resolver.resolve_uri did not return a 405 error when receiving a HEAD')
        
        result = self.c.put(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 405, 'Resolver.resolve_uri did not return a 405 error when receiving a PUT')
        
        result = self.c.delete(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 405, 'Resolver.resolve_uri did not return a 405 error when receiving a DELETE')
        
        result = self.c.options(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 405, 'Resolver.resolve_uri did not return a 405 error when receiving a OPTIONS')
    
    def test_resolve_uri_register_does_not_exist(self):
        result = self.c.get(self.basePath + "something/sent/to/resolver")
        self.assertEqual(result.status_code, 404, 'Resolver.resolve_uri did not return a 404 error when receiving a request for an unknown URI register')
    
    def test_resolve_uri_register_is_remote(self):
        result = self.c.get(self.basePath + "another-registry/to/resolver")
        self.assertEqual(result.status_code, 301, 'Resolver.resolve_uri did not return a 301 redirection when receiving a request for a remote URI register')
    
    def test_resolve_uri_no_matching_rules(self):
        result = self.c.get(self.basePath + "uri-gin/something/sent/to/resolver")
        self.assertEqual(result.status_code, 404, 'Resolver.resolve_uri did not return a 404 error when receiving a request for an unknown URI register')
    
    def test_resolve_uri_multiple_matching_rules(self):
        result = self.c.get(self.basePath + "uri-gin/this/is/a/duplicate/rule")
        self.assertEqual(result.status_code, 500, 'Resolver.resolve_uri did not return a 500 error when receiving a request matching multiple rules')
    
    def test_resolve_uri_no_acceptable_content(self):
        result = self.c.get(self.basePath + "uri-gin/something/twomappings", **{ "HTTP_ACCEPT": 'text/javascript' })
        self.assertEqual(result.status_code, 406, 'Resolver.resolve_uri did not return a 406 error when receiving a request with no acceptable response')
    
    def test_resolve_uri_multiple_acceptable_content(self):
        result = self.c.get(self.basePath + "uri-gin/duplicate/accept/mappings/here", **{ "HTTP_ACCEPT": 'text/html' })
        self.assertEqual(result.status_code, 500, 'Resolver.resolve_uri did not return a 500 error when receiving a request with multiple acceptable responses')
    
    def test_resolve_uri_success_one_group_one_mapping(self):
        result = self.c.get(self.basePath + "uri-gin/something/onegroup/onemapping/success", **{ "HTTP_ACCEPT": 'text/html' })
        self.assertEqual(result['Location'], 'http://elsewhere.com/something', 'Resolver.resolve_uri did not return a 303 redirection to the appropriate location')
    
    def test_resolve_uri_success_one_group_two_mappings(self):    
        result = self.c.get(self.basePath + "uri-gin/something/onegroup/twomappings/success", **{ "HTTP_ACCEPT": 'text/html' })
        self.assertEqual(result['Location'], 'http://elsewhere.com/something', 'Resolver.resolve_uri did not return a 303 redirection to the appropriate location')
    
    def test_resolve_uri_success_two_groups_one_mapping(self):    
        result = self.c.get(self.basePath + "uri-gin/first/twogroups/second/onemapping/success", **{ "HTTP_ACCEPT": 'text/html' })
        self.assertEqual(result['Location'], 'http://elsewhere.com/first--second', 'Resolver.resolve_uri did not return a 303 redirection to the appropriate location')
    
    def test_resolve_uri_success_two_groups_two_mappings(self):    
        result = self.c.get(self.basePath + "uri-gin/first/twogroups/second/twomappings/success", **{ "HTTP_ACCEPT": 'text/html' })
        self.assertEqual(result['Location'], 'http://elsewhere.com/first--second', 'Resolver.resolve_uri did not return a 303 redirection to the appropriate location')
        
    def test_resolve_uri_success_extensions(self):
        result = self.c.get(self.basePath + "uri-gin/first/twogroups/second/twomappings/success.txt")
        self.assertEqual(result['Location'], 'http://fileextension.com/text.txt', 'Resolver.resolve_uri did not return a 303 redirection to the appropriate location when given a file extension')   
        
        
        
        