from django.db import models
from AcceptMapping import AcceptMapping
import mimeparse, re

class RewriteRule(models.Model):
    class Meta:
        app_label = 'uriredirect'
        verbose_name = 'Rewrite Rule'
        verbose_name_plural = 'Rewrite Rules'
        
    register = models.ForeignKey(
        'UriRegister',
        help_text='The URI Register to which this rewrite rule belongs'                             
    )
        
    label = models.CharField(
        max_length=100, 
        help_text='A label for this URI, for recognition in the admin interface'
    )
    
    description = models.TextField(
        blank=True, 
        help_text='(Optional) Free-text description of this URI',
    )
    
    pattern = models.CharField(
        max_length=1000, 
        blank=True, 
        help_text='Regular Expression for this URI to capture. See http://docs.python.org/release/2.5.2/lib/re-syntax.html for syntax guidelines. If you wish for the rule to match based on a requested file extension, please do not end the pattern with a "$" without including logic to explicitly identify a file extension.'
    )

    representations = models.ManyToManyField(
        'MediaType', 
        through='AcceptMapping',
    )
      
    def __unicode__(self):
        return self.pattern
    
    def extension_match(self, requested_extension):        
        accept_mappings = AcceptMapping.objects.filter(
          rewrite_rule = self,
          media_type__file_extension = requested_extension  
        )
        
        if len(accept_mappings) == 0:
          return [], ''
        else:
          return [ mapping.redirect_to for mapping in accept_mappings ], requested_extension
    
    def content_negotiation(self, accept):
        available_mime_types = [ media.mime_type for media in self.representations.all() ]
        if len(available_mime_types) == 0: return [], ''
        
        matching_content_type = mimeparse.best_match(available_mime_types, accept)
        accept_mappings = AcceptMapping.objects.filter(
            rewrite_rule = self,
            media_type__mime_type = matching_content_type
        )
        return [ mapping.redirect_to for mapping in accept_mappings ], matching_content_type
    
    def resolve_url_template(self, requested_uri, url_template):
        match = re.match(self.pattern, requested_uri)
        if match.lastindex != None:
            for i in range(match.lastindex):
                url_template = re.sub('\$' + str(i + 1), match.group(i + 1), url_template)
        return url_template