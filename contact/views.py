# coding=utf-8
from __future__ import print_function
from __future__ import absolute_import, unicode_literals

import uuid

from django.conf import settings
from django.core.mail import send_mass_mail
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def send_contact_email(name, email, subject, message, ref_num):
    ref_str = '#%s' % ref_num
    subject_mail = '%s - [%s] : %s' % (ref_str, name, subject)
    return (subject_mail, message, email, [settings.CONTACT_EMAIL])


def send_confirmation_email(name, email, subject, message, ref_num):
    ref_str = '#%s' % ref_num
    subject_str = '[%s] : ' % subject
    confirmation_mail_ref = subject_str + ' Contact reception confirmation'
    confirmation_mail_body_p1 = \
        _('Dear %s,\n\nWe received your message %s and will answer soon.\n') % (name, ref_str)
    confirmation_mail_body_p2 = \
        _('Your Message:\n\n%s\n\nSincerely,\n\nWAFA Team') % message
    return (
    confirmation_mail_ref, confirmation_mail_body_p1 + confirmation_mail_body_p2, settings.CONTACT_EMAIL, [email])


@api_view(['POST'])
@csrf_protect
def post_message(request):
    if 'POST' == request.method:
        data = request.data
        try:
            ref_num = str(uuid.uuid4())[:10]
            name = data['name']
            email = data['email']
            subject = data['subject']
            message = data['message']

            contact = send_contact_email(name, email, subject, message, ref_num)
            confirmation = send_confirmation_email(name, email, subject, message, ref_num)
            send_mass_mail((contact, confirmation), fail_silently=False)
        except Exception as expt:
            x, y = expt.args
            print('x =', x)
            print('y =', y)
            return Response({'alert': 'error', 'message': 'Server Error ! Please Try Later .'}, status.HTTP_200_OK)

        return Response({'alert': 'success', 'message': _('Your Message has been sent . Wafa Team Thanks You !')},
                        status.HTTP_200_OK)
