from django.db import models

class Request(models.Model):
    path = models.CharField(max_length=1024, help_text = "The relative url to request. Ex: '/search?q=test'", verbose_name = "Request Path")
    comments = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        out = self.path
        for rule in self.requestrule_set.all():
            out += ", " + str(rule)
        return out

class RequestRule(models.Model):
    OPERATOR_CHOICES = (
        (u'contains', u'contains'),
        (u'!contains', u'does not contain')
    )

    request = models.ForeignKey(Request)
    target = models.CharField(max_length = 255)
    operator = models.CharField(max_length = 255, choices = OPERATOR_CHOICES)
    value = models.CharField(max_length = 255, verbose_name = "What to look for")

    @property
    def display_operator(self):
        try:
            operator = dict(RequestRule.OPERATOR_CHOICES)[self.name]
            return operator
        except:
            return self.operator

    def __unicode__(self):
        return "%s %s '%s'" % (self.target, self.display_operator, self.value)
