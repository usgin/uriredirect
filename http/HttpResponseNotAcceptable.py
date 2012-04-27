from django.http import HttpResponse

class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406