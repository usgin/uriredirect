from django.contrib import admin
from uriredirect.models import AcceptMapping

class AcceptMappingInline(admin.TabularInline):
    model = AcceptMapping
    extra = 2