from django.contrib import admin
from models import Request, RequestRule

class RequestRuleInline(admin.TabularInline):
	model = RequestRule
	extra = 1

class RequestAdmin(admin.ModelAdmin):
    model = Request
    inlines = [RequestRuleInline]
admin.site.register(Request, RequestAdmin)
