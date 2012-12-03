from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponsePermanentRedirect, HttpResponseNotAllowed
from uriredirect.models import UriRegister
from uriredirect.http import HttpResponseNotAcceptable, HttpResponseSeeOther

def resolve_uri(request, registry_label, requested_uri, requested_extension):
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    # Determine if this server is aware of the requested registry
    try:
        requested_register = UriRegister.objects.get(label=registry_label)
    except UriRegister.DoesNotExist:
        return HttpResponseNotFound('The requested URI registry does not exist')
    
    # Determine if this server can resolve a URI for the requested registry
    if not requested_register.can_be_resolved:
        return HttpResponsePermanentRedirect(requested_register.construct_remote_uri(requested_uri))
    
    # Find rewrite rules matching the requested uri
    rules = requested_register.find_matching_rules(requested_uri)
    if len(rules) == 0:
        return HttpResponseNotFound('The requested URI does not match any rewrite rules')
    elif len(rules) > 1:
        rule_ids = ",".join([ str(rule.id) for rule in rules ])
        return HttpResponseServerError('The requested URI matches more than one rewrite rule. Here are the rewrite rule IDs: %s' % rule_ids)
    else:
        rule = rules[0]
    
    # If given a file extension, that should be checked first
    if requested_extension != None:
      url_templates, file_extension = rule.extension_match(requested_extension)
      if len(url_templates) == 0: pass
      elif len(url_templates) > 1:
        return HttpResponseServerError('More than one representation is defined for the requested file extension: %s' % file_extension)
      else:
        url_template = url_templates[0]
  
    # Otherwise find the representation that is the best match for the request        
    else:    
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