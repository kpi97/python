#!/usr/bin/env python3
# coding=utf8

import os
import yaml
import smtplib
import urllib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from email import charset
from email.utils import formataddr

import app.pdata

class Sender:
    def send_via_smtp(self, email_from_smtp, key, email_from, email_to, subject, html_text, plain_text, cid_images, attachments):
        """ Отправить сообщение через SMTP

            :param email_from_smtp: имя smtp сервера
            :param key: пароль
            :param email_from: от кого отправляется сообщение
            :param password: пароль почтового ящика
            :param email_to: кому отправляется сообщение
            :param subject: тема сообщения
            :param html_text: текст в формате HTML
            :param plain_text: текст в формате plain
            :param cid_images: пары текста <content-id>, имя-файла
            :param attachments: вложения документа
        """

        # Создать корень сообщения и заполнить его заголовки from, to, и subject
        msgRoot = MIMEMultipart('related')
        msgRoot['Reply-To'] = email_from
        msgRoot['From'] = formataddr((str(Header('FooBar', 'utf-8')), email_from))
        msgRoot['To'] = email_to
        msgRoot['Date'] = formatdate(localtime=True)
        msgRoot['Subject'] = Header(subject, 'utf-8')
        msgRoot['Organization'] = Header('ООО "FooBar"', 'utf-8')
        msgRoot['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101\n Thunderbird/52.5.2"
        msgRoot['Content-Language'] = 'ru'

        # Инкапсулировать plain и HTML версии тела сообщения в части 'alternative',
        # чтобы mail-агенты могли решить, что они хотят отображать
        msgAlternative = MIMEMultipart('alternative')
        # msgAlternative = MIMEMultipart('mixed')


        msgRoot.attach(msgAlternative)

        ch = charset.Charset('utf-8')
        ch.body_encoding = '8bit'

        msgHtml = MIMEText(plain_text, 'plain', 'utf-8')
        msgAlternative.attach(msgHtml)
        msgHtml = MIMEText(html_text, 'html', 'utf-8')
        msgAlternative.attach(msgHtml)

        for cid, filename in cid_images:
            with open(filename, "rb") as f:
                msgImage = MIMEImage(f.read())
                msgImage.add_header('Content-ID', '<' + cid + '>')
                msgImage.add_header('Content-Disposition', 'inline; filename="' + cid + '"')
                msgRoot.attach(msgImage)

        for base, fname in attachments or []:
            filename = os.path.join(base, fname)
            with open(filename, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="pdf", name=Header(fname, maxlinelen=68).encode())

            name = "utf-8''" + urllib.parse.quote(fname.encode('utf-8'))
            # После закрытия файла
            part['Content-Disposition'] = 'attachment;\n' + self.encode_filename(name)
            msgRoot.attach(part)

        s = msgRoot.as_string()
        #with open("/home/artem/tmp/tst.eml", "w") as f:
        #    f.write(s)

        if 1:
            print(email_from_smtp)
            server = smtplib.SMTP_SSL(email_from_smtp)
            server.ehlo(email_from)
            server.login(email_from, key)
            server.sendmail(email_from, email_to, s)
            server.sendmail(email_from, email_from, s)
            server.quit()


    def encode_filename(self, name):
        if len(name) <= 61:
            return " filename*0*=" + name
        else:
            dst = [" filename*0*=" + name[:61] + ';']
            i = 1
            name = name[61:]
            while len(name) > 60:
                part = name[:60]
                name = name[60:]
                end_semicol = ';' if len(name) > 0 else ''
                dst.append(" filename*" + str(i) + "*=" + part + end_semicol)
                i += 1

            if len(name) > 0:
                dst.append(" filename*" + str(i) + "*=" + name)

        return "\n".join(dst)


    def send_from_config(self, config):
        with open(config["text"], 'r') as f:
            text = f.read()
        with open(config["html"], 'r') as f:
            html = f.read()
        attachments = [(config["attach_path"], config["attach"])]

        with open(config["images"], 'r') as f:
            images = [(x["img"]["cid"], x["img"]["file"]) for x in yaml.load(f)["collection"]]

        self.send_via_smtp(email_from_smtp=pdata.data[config["from"]]["smtp"],
                           key=pdata.data[config["from"]]["key"],
                           email_from=config["from"],
                           email_to=config["to"],
                           subject=config["subject"],
                           html_text=html,
                           plain_text=text,
                           cid_images=images,
                           attachments=attachments)



if __name__ == '__main__':
    pass




