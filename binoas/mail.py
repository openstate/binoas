#!/usr/bin/env python
from sendgrid.helpers.mail import Mail, Email, Personalization, Content
import sendgrid


def send_mail(api_key, subject, content, to=['developers@openstate.eu']):
    sg = sendgrid.SendGridAPIClient(apikey=api_key)

    mail = Mail(
        Email("developers@openstate.eu", "Open State Foundation"),
        subject, Email(to[0], to[0]))

    mail.add_content(Content("text/plain", content))
    mail.add_content(Content("text/html", content))

    sg.client.mail.send.post(request_body=mail.get())
