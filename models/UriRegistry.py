from django.db import models
import re

class UriRegistry(models.Model):
    class Meta:
        app_label = 'uriredirect'
        verbose_name = 'URI Registry'
        verbose_name_plural = 'URI Registries'
        
    label = models.CharField(
        max_length=50,
        unique=True,
        help_text='A label that uniquely identifies a particular URI registry'                                  
    )
    
    url = models.URLField(
        help_text='The absolute URL of a server at which this URI registry can be reached'                      
    )
    
    can_be_resolved = models.BooleanField(
        help_text='Determines whether this server is capable of resolving URIs for this URI registry'                                       
    )
    
    def __unicode__(self):
        return self.label
    
    def find_matching_rules(self, requested_uri):
        return [ rule for rule in self.rewriterule_set.all() if re.match(rule.pattern, requested_uri) != None ]