from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from url_watcher.models import Request
from url_watcher.watcher import check_request_rules, create_django_response

class Command(BaseCommand):

    help = "Django Url Watcher management command to check all of the requests and e-mail results"

    option_list = BaseCommand.option_list + (make_option('-n', '--dry-run',
            action="store_true",
            default=False,
            dest="dry_run",
            help="Just output the results, don't email"
        ),
        make_option('-e', '--email',
            dest = "email",
            help="email to send the results to. defaults to settings.URL_WATCHER_EMAILTO then settings.ADMINS"
        )
    )


    def handle(self, *args, **options):
        output = ""
        for request in Request.objects.all():
            if options["verbosity"] >= 2:
                print "Checking %s" % str(request)
                django_response = create_django_response(request.path)
                errors = check_request_rules(request, django_response)

                if len(errors) > 0:
                    output += "\n".join(errors)


        if options["dry_run"]:
            print output 
            return

        # Email
        if options["email"]:
            emails = [options["email"]]
        else:
            emails = getattr(settings, "URL_WATCHER_EMAIL_TO", dict(settings.ADMINS).values())
        from_email = getattr(settings, "URL_WATCHER_EMAIL_FROM", settings.DEFAULT_FROM_EMAIL)
        subject = "Django Url Watcher found a problem" 
        message = output

        print "Errors found, emailing", emails
        send_mail(subject=subject, message=message, from_email = from_email, recipient_list=emails)
    
