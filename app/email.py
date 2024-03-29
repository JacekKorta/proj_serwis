from flask import render_template
from flask_mail import Message

from app import app, mail


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_new_issue(user, issue):
    # Sending mail about new issue
    subject = '[SERWIS] {} - nowe zgłoszenie serwisowe'.format(issue.id)
    admin_adres = app.config['ADMIN'][0]
    warehouse_adres = app.config['WAREHOUSE'][0]
    send_mail(subject,
            sender=app.config['SENDER'][0],
            recipients=[user.email,admin_adres,warehouse_adres],
            text_body= render_template('email/email_new_issue.txt', issue=issue),
            html_body = render_template('email/email_new_issue.html', issue=issue))


def send_delayed_payments(customer, data):
    # Sending mail about delayed payments information
    subject = '{} - Zaległe płatności dla ETI'.format(customer.code)
    office = app.config['OFFICE'][0]
    send_mail(subject,
              sender=office,
              recipients=[office, customer.email],
              text_body=render_template('email/email_delayed_payments.txt', data=data),
              html_body=render_template('email/email_delayed_payments.html', data=data))
