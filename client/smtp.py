import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys


def send(to, subject, plainBody, htmlBody):
    host = None
    port = 587
    username = None
    password = None
    secure = False
    smtp = config.smtp
    smtps = config.smtps

    if smtp != None and len(smtp) > 0:
        host = smtp
    elif smtps != None and len(smtps) > 0:
        host = smtps
        port = 465
        secure = True
    else:
        raise "The SMTP server is missing."

    atIndex = host.rfind("@")

    if atIndex >= 0:
        username = host[:atIndex]
        host = host[atIndex+1:]

        if username.find(":") >= 0:
            password = username[username.find(":") + 1:]
            username = username[:username.find(":")]

    portIndex = host.find(":")

    if portIndex >= 0:
        port = int(host[portIndex+1:])
        host = host[:portIndex]

    if config.debug:
        print("SMTP Host: " + host)
        print("SMTP Port: " + str(port))
        print("SMTP Username: " + username)
        print("SMTP Password: " + ("***" if password else ""))
        print("SMTP Secure connection: " + str(secure))
    try:
        server = smtplib.SMTP_SSL(
            host, port) if secure else smtplib.SMTP(host, port)
        server.ehlo()

        if username and password:
            server.login(username, password)

        msg = toPlainMessage(username, to, subject, plainBody, htmlBody)

        server.sendmail(username, [to], msg.as_string())
        server.close()
    except:
        print "Failed to send email: " + unicode(sys.exc_info()[0])
        raise


def toPlainMessage(frm, to, subject, plainBody, htmlBody):
    msg = MIMEMultipart("alternative")

    msg.set_charset("utf8")

    msg["FROM"] = frm
    msg["To"] = to
    msg["Subject"] = Header(subject, "UTF-8").encode()
    # msg["Content-Type"] = "text/plain"

    plainBody = plainBody.replace("\r\n", "\n")
    plainBody = plainBody.replace("\n", "\r\n")
    plainPart = MIMEText(plainBody, "plain", "UTF-8")

    msg.attach(plainPart)

    htmlPart = MIMEText(htmlBody, "html", "UTF-8")

    msg.attach(htmlPart)

    return msg
