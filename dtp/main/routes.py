from flask import Blueprint, render_template, request
from flask_login import current_user
from dtp.models import Announcement, Unattendance
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    announcements = Announcement.query.all()
    if current_user.is_authenticated:
        last_5_unattendances = Unattendance.query.filter_by(student_id=current_user.id)\
        .order_by(desc(Unattendance.id))\
        .limit(5).all()
    else:
        last_5_unattendances = None

    print(f"{request.remote_addr} bağlandı.")
    return render_template('home.html', title='DTP', announcements=announcements, unattendances = last_5_unattendances)