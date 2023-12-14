from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

def send_mail_for_verify(user):
    context = {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(
        'verify/verify_user.html',
        context=context,
    )
    email = EmailMessage(
        'Veryfi email',
        message,
        to=[user.email],
    )
    email.send()