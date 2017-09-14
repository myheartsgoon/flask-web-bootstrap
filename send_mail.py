#-*- coding: utf8 -*-
from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread
import os

#Send email asynchronous
def send_async_mail(app, msg, mail):
    with app.app_context():
        mail.send(msg)


def send_mail(to, user, token):
    app = current_app._get_current_object()
    app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮件服务器地址
    app.config['MAIL_PORT'] = 465  # 邮件服务器端口
    app.config['MAIL_USE_TLS'] = False  # 启用 TLS
    app.config['MAIL_USE_SSL'] = True  # 启用 SSL
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    mail = Mail(app)
    msg = Message('Confirm Your Account', sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template('confirm.txt', user=user, token=token)

    thr = Thread(target=send_async_mail, args=[app, msg, mail])
    thr.start()
    return '<h1>OK!</h1>'

