from django.contrib import admin
from AcceptMappingInline import AcceptMappingInline

class RewriteRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'pattern', 'register')
    list_filter = ('register',)
    search_fields = ('label', 'pattern')
    
    fieldsets = [
        ('Rule Metadata', {
            'fields': ['register', 'label', 'description']
        }),
        ('URI Pattern', {
            'fields': ['pattern']                 
        })
    ]
    
    inlines = [AcceptMappingInline]
    
    