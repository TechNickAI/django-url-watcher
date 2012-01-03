from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.utils.importlib import import_module
from models import Request

ACCEPTABLE_STATUSES = [200]


def create_django_response(watcher_request):
    """ Returns a django response object for the specified path """
    client = UrlWatcherClient()

    if watcher_request.login_as_user is not None:
        client.login_as(watcher_request.login_as_user)

    return client.get(watcher_request.path)


def check_request_rules(watcher_request, django_response):
    errors = []
    if django_response.status_code not in ACCEPTABLE_STATUSES:
        errors.append("For %s, response status code was %s" % (watcher_request.path, django_response.status_code))

    for rule in watcher_request.requestrule_set.all():
        assert(rule.target in ["content"]) # for now, we only support checking the response content
        if rule.target == "content":
            if not check_operator(django_response.content, rule.operator, rule.value):
                errors.append("For %s, the following test failed: %s" % (watcher_request.path, str(rule)))

    return errors


def check_operator(to_check, operator, value):

    def int_or_0(value) :
        try: 
            return int(value)
        except:
            return 0
        
    if operator == "contains":
        return value.lower() in to_check.lower()
    elif operator == "!contains":
        return value.lower() not in to_check.lower()
    elif operator == "=":
        return value == to_check
    elif operator == "!=":
        return value != to_check
    elif operator == "<":
        return int_or_0(to_check) < int_or_0(value)
    elif operator == ">":
        return int_or_0(to_check) > int_or_0(value)
    else:
        raise Exception("Invalid operator - %s" % operator)


class UrlWatcherClient(Client):
    """ Extend the default Django test client for special stuff we need """

    def login_as(self, user):
        """ 
        Sets the Factory to appear as if it has successfully logged into a site.

        Returns True if login is possible; False if the provided credentials
        are incorrect, or the user is inactive, or if the sessions framework is
        not available.

        Note: We would have liked to have used the native 'login' function, 
        but that uses the authenticate function, which requires the password.
        """

        # Innocent Hack to set the backend. Normally "authenticate" must be called to do this. See
        # https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.login
        user.backend = "django.contrib.auth.backends.ModelBackend"

        # From here on out, it's identical to the native 'login' function
        if user and user.is_active \
                and 'django.contrib.sessions' in settings.INSTALLED_APPS:
            engine = import_module(settings.SESSION_ENGINE)

            # Create a fake request to store login details.
            request = HttpRequest()
            if self.session:
                request.session = self.session
            else:
                request.session = engine.SessionStore()

            login(request, user)

            # Save the session values.
            request.session.save()

            # Set the cookie to represent the session.
            session_cookie = settings.SESSION_COOKIE_NAME
            self.cookies[session_cookie] = request.session.session_key
            cookie_data = {
                'max-age': None,
                'path': '/',
                'domain': settings.SESSION_COOKIE_DOMAIN,
                'secure': settings.SESSION_COOKIE_SECURE or None,
                'expires': None,
            }
            self.cookies[session_cookie].update(cookie_data)

            return True
        else:
            return False
