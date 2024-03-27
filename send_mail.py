import smtplib
import os
import mimetypes

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart

from constants import (
    EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
)


def send_email(
        addr_to: str,
        theme_message: str,
        text_message: str,
        files: list | tuple | set | None = None):
    '''Отправка сообщения через почтовый ящик,
    в том числе возможно передавать файлы'''
    addr_from = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = theme_message

    body = text_message
    msg.attach(MIMEText(body, 'plain'))

    if files:
        process_attachement(msg, files)

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()


def process_attachement(msg, files):
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.exists(f):
            dir = os.listdir(f)
            for file in dir:
                attach_file(msg, f+"/"+file)


def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filepath) as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)
