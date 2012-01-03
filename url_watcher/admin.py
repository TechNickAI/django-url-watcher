from django.contrib import admin
from models import Request, RequestRule

class RequestRuleInline(admin.TabularInline):
	model = RequestRule
	extra = 1

class RequestAdmin(admin.ModelAdmin):

    def request_rules(self, obj):
        out = []
        for rule in obj.requestrule_set.all():
            out.append(str(rule))
        if len(out) == 0:
            return "-"
        else:
            return ", ".join(out)

    def login_as(self, obj):
        if obj.login_as_user:
            return str(obj.login_as_user)
        else:
            return "Anonymous"

    inlines = [RequestRuleInline]
    list_display = ('path', 'login_as', 'request_rules')
    model = Request
    ordering = ["-created_at"]
    raw_id_fields = ["login_as_user"]
    search_fields = ['path', 'login_as_user__username']
admin.site.register(Request, RequestAdmin)
