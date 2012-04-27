from django.http import HttpResponse

class HttpResponseSeeOther(HttpResponse):
    status_code = 303
    
    def __init__(self, location):
        HttpResponse.__init__(self)
        self['Location'] = location