from django.test import TestCase
from uriredirect.models import RewriteRule, UriRegister, AcceptMapping, MediaType

class RewriteRuleTestCase(TestCase):
    fixtures = ['test_mediatype.json', 'test_uriregister.json', 'test_rewriterule.json', 'test_acceptmapping.json']
    
    def test_content_negotiation_without_mappings(self):
        rule = RewriteRule.objects.get(label='No Mappings')
        
        result = rule.content_negotiation('text/plain')
        self.assertEqual(result[0], [], 'RewriteRule.content_negotiation on a rule with no AcceptMappings did not return an empty array')
        self.assertEqual(result[1], '', 'RewriteRule.content_negotiation on a rule with no AcceptMappings did not return a blank acceptable content-type')
    
    def test_content_negotiation_exact_match(self):
        rule = RewriteRule.objects.get(label='Two Mappings')
        
        result = rule.content_negotiation('image/png')
        self.assertEqual(result[0], ['http://domain.com/image.png'], 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct URL')
        self.assertEqual(result[1], 'image/png', 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct acceptable content-type')
    
        result = rule.content_negotiation('text/plain')
        self.assertEqual(result[0], ['http://domain.com/text.txt'], 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct URL')
        self.assertEqual(result[1], 'text/plain', 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct acceptable content-type')
    
    def test_content_negotiation_inexact_match(self):
        rule = RewriteRule.objects.get(label='Two Mappings')
        
        result = rule.content_negotiation('image/*')
        self.assertEqual(result[0], ['http://domain.com/image.png'], 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct URL when the accept header was inexact')
        self.assertEqual(result[1], 'image/png', 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct acceptable content-type when the accept header was inexact')
        
        result = rule.content_negotiation('text/*')
        self.assertEqual(result[0], ['http://domain.com/text.txt'], 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct URL when the accept header was inexact')
        self.assertEqual(result[1], 'text/plain', 'RewriteRule.content_negotiation on a rule with multiple mappings did not return the correct acceptable content-type when the accept header was inexact')
    
    def test_content_neogtiation_no_match(self):
        rule = RewriteRule.objects.get(label='Two Mappings')
        
        result = rule.content_negotiation('text/javascript')
        self.assertEqual(result[0], [], 'RewriteRule.content_negotiation on a rule with multiple mappings returned a match when there should have been none')
        self.assertEqual(result[1], '', 'RewriteRule.content_negotiation on a rule with multiple mappings returned an acceptable content-type when there should have been none')
    
    def test_resolve_uri_template_no_capture_groups(self):
        rule = RewriteRule.objects.get(label='No Capture Groups')
        
        result = rule.resolve_url_template('1234/nogroups', 'http://domain.com/')
        self.assertEqual(result, 'http://domain.com/', 'RewriteRule.resolve_url_template did not return the correct value for a pattern with no capture groups')
        
    def test_resolve_uri_template_one_capture_group(self):
        rule = RewriteRule.objects.get(label='Single Capture Group')
        
        result = rule.resolve_url_template('something/onegroup', 'http://domain.com/$1')
        self.assertEqual(result, 'http://domain.com/something', 'RewriteRule.resolve_url_template did not return the correct value for a single capture group')
      
    def test_resolve_uri_template_multiple_capture_groups(self):
        rule = RewriteRule.objects.get(label='Multiple Capture Groups')
        
        result = rule.resolve_url_template('35412/letters', 'http://domain.com/$1--$2')
        self.assertEqual(result, 'http://domain.com/35412--letters', 'RewriteRule.resolve_url_template did not return the correct value for multiple capture groups')  
        
        