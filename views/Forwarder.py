from django.http import HttpResponsePermanentRedirect

def forward_request(uri_registry, requested_uri):    
    return HttpResponsePermanentRedirect("/".join[uri_registry.url.strip("/"), requested_uri])