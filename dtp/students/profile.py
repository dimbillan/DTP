from flask import render_template, request, g
from flask_login import login_required, current_user

from dtp import logger
from dtp.students.utils import *

from . import students

@students.before_request
def get_real_ip():
    g.real_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr

@students.route('/profile')
@login_required
def profile():
    logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] profilini görüntüledi.") 
    return render_template('students/profile.html', title='Profil', student=current_user)