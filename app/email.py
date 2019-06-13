from flask import render_template
from flask_mail import Message
from app import app, mail

def send_mail (subject, sender, recipients, text_body, html_body ):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_new_issue(user,issue):
    subject = 'Nowe zgłoszenie serwisowe nr {}'.format(issue.id)
    admin_adres = 'j.korta@janome.pl'
    warehouse_adres = 'jacek.korta@gmail.com'
    sender = 'eaters@o2.pl'
    send_mail(subject,
            sender=sender,
            recipients=[user.email,admin_adres,warehouse_adres],
            text_body= render_template('email/new_issue.txt', issue=issue),
            html_body = render_template('email/new_issue.html', issue=issue))
