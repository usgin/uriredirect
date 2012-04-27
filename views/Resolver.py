from django.http import HttpResponseNotFound, HttpResponseServerError
from uriredirect.models import UriRegistry
from uriredirect.http import HttpResponseNotAcceptable, HttpResponseSeeOther
from Forwarder import forward_request

def resolve_uri(request, registry_label, requested_uri):
    # Determine if this server is aware of the requested registry
    try:
        requested_registry = UriRegistry.objects.get(label=registry_label)
    except UriRegistry.DoesNotExist:
        return HttpResponseNotFound('The requested URI registry does not exist')
    
    # Determine if this server can resolve a URI for the requested registry
    if not requested_registry.can_be_resolved:
        return forward_request(requested_registry, requested_uri)
    
    # Find rewrite rules matching the requested uri
    rules = requested_registry.find_matching_rules(requested_uri)
    if len(rules) == 0:
        return HttpResponseNotFound('The requested URI does not match any rewrite rules')
    elif len(rules) > 1:
        rule_ids = ",".join([ rule.id for rule in rules ])
        return HttpResponseServerError('The requested URI matches more than one rewrite rule. Here are the rewrite rule IDs: %s' % rule_ids)
    else:
        rule = rules[0]
        
    # Find the representation that is the best match for the request
    accept = request.META.get('HTTP_ACCEPT', '*')
    url_templates, content_type = rule.content_negotiation(accept)
    if len(url_templates) == 0:
        return HttpResponseNotAcceptable('No representations is acceptable for the requested MIME type: %s' % accept)
    elif len(url_templates) > 1:
        return HttpResponseServerError('More than one representation is defined for the acceptable MIME type: %s' % content_type)
    else:
        url_template = url_templates[0]
        
    # Convert the URL template to a resolvable URL
    url = rule.resolve_url_template(requested_uri, url_template)
    
    # Perform the redirection
    return HttpResponseSeeOther(url)