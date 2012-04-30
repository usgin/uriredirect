from django.test import TestCase
from uriredirect.models import RewriteRule, UriRegister

class UriRegisterTestCase(TestCase):
    fixtures = ['test_mediatype.json', 'test_uriregister.json', 'test_rewriterule.json']
    
    def test_find_matching_rules_correct_match(self):
        usginRegister = UriRegister.objects.get(label='uri-gin')
        
        matchingRule = RewriteRule.objects.get(label='Matching Rule')
        
        for uri in [ 'whatever/002', 'anything/98213']:
            result = usginRegister.find_matching_rules(uri)
            self.assertEqual(result, [ matchingRule ], 'UriRegistry.find_matching_rules returned an incorrect match')
            
    def test_find_matching_rules_no_match(self):
        usginRegister = UriRegister.objects.get(label='uri-gin')
        
        for uri in [ '' ]:
            result = usginRegister.find_matching_rules(uri)
            self.assertEqual(result, [], 'UriRegistry.find_matching_rules returned a match when it should not have')
        
        
        for uri in [ 'wutwut', '/wut/wut/', 'somewhere/out/there/']:
            pass
    def test_find_matching_rules_multiple_matches(self):
        usginRegister = UriRegister.objects.get(label='uri-gin')
        
        matchingRule = RewriteRule.objects.get(label='Matching Rule')
        notMatchingRule = RewriteRule.objects.get(label='Not Matching Rule')
        
        for uri in [ '123/456' ]:
            result = usginRegister.find_matching_rules(uri)
            self.assertTrue(matchingRule in result, 'UriRegistry.find_matching_rules did not return multiple rules matching a pattern that should have')
            self.assertTrue(notMatchingRule in result, 'UriRegistry.find_matching_rules did not return multiple rules matching a pattern that should have')
            
    def test_construct_remote_uri(self):
        usginRegister = UriRegister.objects.get(label='uri-gin')
        
        result = usginRegister.construct_remote_uri('wutwut')
        self.assertEqual(result, 'http://localhost:8000/wutwut')
        
        result = usginRegister.construct_remote_uri('/wut/wut/')
        self.assertEqual(result, 'http://localhost:8000/wut/wut/')
        
        result = usginRegister.construct_remote_uri('somewhere/out/there/')
        self.assertEqual(result, 'http://localhost:8000/somewhere/out/there/')