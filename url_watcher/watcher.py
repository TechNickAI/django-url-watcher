from django.test.client import Client
from models import Request

ACCEPTABLE_STATUSES = [200]

def check_request_rules(watcher_request):

    client = Client()
    errors = []

    response = client.get(watcher_request.path)
    if response.status_code not in ACCEPTABLE_STATUSES:
        errors.append("For %s, response status code was %s" % (watcher_request.path, response.status_code))


    for rule in watcher_request.requestrule_set.all():
        assert(rule.target in ["content"]) # for now, we only support checking the response content
        if rule.target == "content":
            if not check_operator(response.content, rule.operator, rule.value):
                errors.append("For %s, the following test failed: %s" % (watcher_request.path, str(rule)))

    return (response, errors)


def check_operator(to_check, operator, value):
    if operator == "contains":
        return value.lower() in to_check.lower()
    elif operator == "!contains":
        return value.lower() not in to_check.lower()
    else:
        raise Exception("Invalid operator - %s" % operator)
