from django.db import models

class AcceptMapping(models.Model):
    class Meta:
        app_label = 'uriredirect'
        verbose_name = 'Accept-Mapping'
        verbose_name_plural = 'Accept-Mapping'
        
    rewrite_rule = models.ForeignKey('RewriteRule')
    media_type = models.ForeignKey(
        'MediaType',
        verbose_name = 'Media Type'
    )
    redirect_to = models.CharField(
        max_length=2000,
        help_text='The URL or URL template to which the specified Representation Type should redirect.'
    )
    
    def __unicode__(self):
        return self.media_type.mime_type