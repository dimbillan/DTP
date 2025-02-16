from flask import render_template
from flask_login import login_required, current_user

from dtp.students.utils import *

from . import students

@students.route('/profile')
@login_required
def profile():
    return render_template('students/profile.html', title='Profil', student=current_user)