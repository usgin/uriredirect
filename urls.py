from django.conf.urls import patterns, url

urlpatterns = patterns('uriredirect.views',
    url(r'^(?P<registry_label>.+?)/(?P<requested_uri>.+?)(?P<requested_extension>\.[a-zA-Z]{3,4})?$', 'resolve_uri'),                  
)                       