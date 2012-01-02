from django.db import models

class Request(models.Model):
    path = models.CharField(max_length=1024, help_text = "The url to request, starting with /. Ex: '/search?q=test'")
    comments = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

class RequestTest(models.Model):
    OPERATOR_CHOICES = (
        (u'=', u'Equals'),
        (u'>', u'Greater'),
        (u'<', u'Less'),
        (u'contains', u'contains'),
        (u'does not contain', u'does not contain')
    )

    request = models.ForeignKey(Monitor)
    target = models.CharField(max_length = 255)
    operator = models.CharField(max_length = 255, choices = OPERATOR_CHOICES)
    value = models.CharField(max_length = 255)
