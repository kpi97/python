#!/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
import html as utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Response
from flask import render_template, redirect, url_for
from app import app, send, pdata
from flask_cors import CORS

CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', send_email='/send')


def send_msg_from_site(name, email, message):
	sender = send.Sender()
	html_text="""<html>
	<body>
		<h1>From: """ + name + """ </h1>
		<h2>To: """ + email + """ </h2>
		<h3>Message: """ + message + """ </h3>
	</body>
	</html>"""
	sender.send_via_smtp(email_from_smtp=pdata.from_smtp,
                           key=pdata.from_key,
                           email_from=pdata.from_email,
                           email_to=pdata.to_email,
                           subject="message from flask",
                           html_text=html_text,
                           plain_text=name+ " " + email + " " + message,
                           cid_images=[],
                           attachments=[])
    


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route('/send', methods=['POST'])
def send_email():
    def strip_size(l, x):
        if len(x) > l:
            return x[:l]
        else:
            return x

    def escape_strip(l, x):
        text = str(request.form[x])
        if len(text) == 0:
            return ""
        return (utils.escape(strip_size(l, text))).strip()

    name = escape_strip(1000, 'send-name')
    email = escape_strip(1000, 'send-email')
    message = escape_strip(10000, 'send-message')

    if len(name) == 0 or len(email) == 0 or len(message) == 0:
        return "Ошибка. Поля формы не заполнены."

    send_msg_from_site(name, email, message)
    return redirect(url_for('email_response'))

@app.route('/response')
def email_response():
	return render_template('response.html', company="FooBar")