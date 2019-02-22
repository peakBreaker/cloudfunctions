#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import os


FROM_ADDR = 'noreply.peakbreaker@gmail.com'
toaddrs = 'andershurum@gmail.com'
USERNAME = os.environ.get('BOT_EMAIL_USER', None)
PASSWORD = os.environ.get('BOT_EMAIL_PASSWORD', None)
SECRET = os.environ.get('SUPERSECRET', None)
base_msg = "\r\n".join([
  "From: {username}".format(username=USERNAME),
  "To: {toaddr}",
  "Subject: {subject}",
  "",
  "{msg}"
  ])


def send_email(toaddr='andershurum@gmail.com',
               subject='AUTOMAIL: Default subject',
               msg='there was no provided msg'):
    """Sends an email to some muck"""

    # authenticate with server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(USERNAME, PASSWORD)

    # send the mails
    sendmsg = base_msg.format(subject=subject, msg=msg, toaddr=toaddr)
    print("sending mail \n %s" % sendmsg)
    server.sendmail(USERNAME, toaddr, sendmsg)

    # Exit
    server.quit()


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'POST':
        print("Got HTTP POST!")
        if request.form and 'secret' in request.form:
            print('Found secret in post')
            print(request.form['secret'])
            if request.form['secret'] == SECRET:
                print('Sending mail')
                send_email(toaddrs=request.form.get('toaddr', 'andershurum@gmail.com'),
                           msg=request.form.get('msg', 'no provided message'))
                return "Correct secret, sent a message!"
            else:
                return "You provided wrong message"
        else:
            return "You did not provide a secret"
    elif request.method == 'GET':
        return """<form action="/sendmail" method="post">
                    <input type="text" name="secret" placeholder="secret"><br>
                    <input type="text" name="toaddr" placeholder="receiver"><br>
                    <input type="text" name="msg" placeholder="message"><br>
                    <input type="submit">
                   </form>"""
    else:
        return 'Invalid HTTP arg'


if __name__ == '__main__':
    send_email()
