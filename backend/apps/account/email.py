from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings


def send_email_to_user(subject, template_name, user, token=None, domain=None):
    app, ext = template_name.split('/')[0], template_name.split('.')[-1]
    if ext == 'html' and app in [app.split('.')[-1] for app in settings.LOCAL_APPS]:
        body = render_to_string(
            template_name, {
                'user': user,
                'domain': domain or None,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)) or None,
                'token': token or None
            }
        )
    else:
        body = template_name
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.send()