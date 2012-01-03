from django.db import models

class Request(models.Model):
    path = models.CharField(max_length=1024, help_text = "The url to request, starting with /. Ex: '/search?q=test'", verbose_name = "Request Path")
    comments = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

class RequestRule(models.Model):
    OPERATOR_CHOICES = (
        (u'contains', u'contains'),
    )

    request = models.ForeignKey(Request)
    target = models.CharField(max_length = 255)
    operator = models.CharField(max_length = 255, choices = OPERATOR_CHOICES)
    value = models.CharField(max_length = 255, verbose_name = "What to look for")
