#-*- coding: utf8 -*-
from flask import Blueprint, current_app
from flask_mail import Mail, Message
from threading import Thread
import os

mail_bp = Blueprint('mail', __name__, template_folder='templates')

#Send email asynchronous
def send_async_mail(app, msg, mail):
    with app.app_context():
        mail.send(msg)


#Encapsulate email
@mail_bp.route('/mail')
def send_mail():
    app = current_app._get_current_object()
    app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮件服务器地址
    app.config['MAIL_PORT'] = 465  # 邮件服务器端口
    app.config['MAIL_USE_TLS'] = False  # 启用 TLS
    app.config['MAIL_USE_SSL'] = True  # 启用 SSL
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or '408168042@qq.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'ugoarxyzbardbhdb'
    mail = Mail(app)
    msg = Message('Hi', sender='408168042@qq.com', recipients=['408168042@qq.com'], html='<b>Hello Web!</b>',
                  body='The first email!')

    thr = Thread(target=send_async_mail, args=[app, msg, mail])
    thr.start()
    return '<h1>OK!</h1>'

