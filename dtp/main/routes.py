from flask import Blueprint, render_template, request, g
from flask_login import current_user

from sqlalchemy import desc

from dtp import logger
from dtp.models import Announcement, Unattendance

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    real_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr

    announcements = Announcement.query.all()

    if current_user.is_authenticated:
        logger.info(f"{request.method} - [IP: {real_ip}] - [{current_user.name}({current_user.id})] anasayfada.")  
        
        last_5_unattendances = Unattendance.query.filter_by(student_id=current_user.id)\
        .order_by(desc(Unattendance.id))\
        .limit(5).all()
    
    else:
        logger.info(f"{request.method} - [IP: {real_ip}] - [Giriş Yapmamış Kullanıcı] anasayfada.")  
        last_5_unattendances = None

    return render_template('home.html', title='DTP', announcements=announcements, unattendances = last_5_unattendances)