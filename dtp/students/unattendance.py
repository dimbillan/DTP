from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user

from sqlalchemy.orm import joinedload

from dtp import db
from dtp.models import Weeks, Unattendance, Lecture
from dtp.students.forms import GetUnattendancesForm, UpdateUnattendancesForm
from dtp.students.utils import *

from . import students

@students.route('/unattendance', methods=['GET', 'POST'])
@login_required
def unattendance():
    form_get = GetUnattendancesForm()
    form_update = UpdateUnattendancesForm()

    lectures = Lecture.query.all()
    weeks = Weeks.query.all()

    form_get.lecture.choices = [(lecture.id, lecture.name) for lecture in lectures]

    form_update.lecture.choices = [(lecture.id, lecture.name) for lecture in lectures] 
    form_update.week.choices= [(week.id, week.week_name) for week in weeks]

    unattendances = Unattendance.query.filter_by(student_id=current_user.id).all()

    if form_update.validate_on_submit():
        lecture_id = form_update.lecture.data
        week_id = form_update.week.data

        attendance = Unattendance.query.filter_by(student_id=current_user.id, lecture_id=lecture_id, week_id=week_id).first()

        if attendance:
            flash(f'Devamsızlık kaydı {attendance.lecture.name} dersi için {week_id}. haftada zaten mevcut', 'danger')
            return redirect(url_for('students.unattendance'))
        
        else:
            new_unattendance = Unattendance(student_id=current_user.id, lecture_id=lecture_id, week_id=week_id)

            db.session.add(new_unattendance)
            db.session.commit()

            flash(f'Devamsızlık kaydı {new_unattendance.lecture.name} dersi için {week_id}. haftaya eklendi', 'success')

            return redirect(url_for('students.unattendance'))
        
    if form_get.validate_on_submit():
        lecture_id = form_get.lecture.data
        unattendances = Unattendance.query.filter_by(student_id=current_user.id, lecture_id=lecture_id).all()

    return render_template('students/unattendance.html', title='Devamsızlıklar', form_get=form_get, form_update= form_update, unattendances=unattendances)

@students.route('/unattendance/delete/<int:id>', methods=['POST'])
def delete_unattendance(id):

    devamsizlik = Unattendance.query.options(joinedload(Unattendance.lecture)).get(id)

    if devamsizlik:
        db.session.delete(devamsizlik)
        db.session.commit()
        flash(f'Devamsızlık kaydı {devamsizlik.lecture.name} dersi için {devamsizlik.week_id}. haftadan silindi', 'info')

    return redirect(url_for('students.unattendance'))