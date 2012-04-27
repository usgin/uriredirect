from django.contrib import admin
from AcceptMappingInline import AcceptMappingInline

class RewriteRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'pattern', 'registry')
    list_filter = ('registry',)
    search_fields = ('label', 'pattern')
    
    fieldsets = [
        ('Rule Metadata', {
            'fields': ['registry', 'label', 'description']
        }),
        ('URI Pattern', {
            'fields': ['pattern']                 
        })
    ]
    
    inlines = [AcceptMappingInline]
    
    