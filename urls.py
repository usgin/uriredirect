from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('uriredirect.views',
    url(r'^(?P<registry_label>.+?)/(?P<requested_uri>.+)$', 'resolve_uri'),                  
)                       