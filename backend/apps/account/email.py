from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings


def send_email_activation_account(current_site, user, token, subject, template_name):
    email_body_activate = render_to_string(template_name, {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        }
    )
    email = EmailMessage(
        subject=subject,
        body=email_body_activate,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.send()

def send_email_activation_account_success(current_site, user, subject, template_name):
    email_body_activate_success = render_to_string(template_name, {'domain': current_site,})
    email = EmailMessage(
        subject=subject,
        body=email_body_activate_success,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.send()