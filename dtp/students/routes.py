from flask import Blueprint, redirect, request, render_template, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.orm import joinedload

from dtp import db, bcrypt
from dtp.models import Student, Weeks, Unattendance, Lecture
from dtp.students.forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm, GetUnattendancesForm, UpdateUnattendancesForm, AddLecture
from dtp.students.utils import *

students = Blueprint('students', __name__)

@students.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Giriş Başarısız. Öğrenci numaranızı ve şifrenizi kontrol edin.', 'danger')
    return render_template('login.html', title='Giriş Yap', form=form)

@students.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(email=form.email.data, name=form.name.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Hesabınız oluşturuldu. Artık giriş yapabilirsiniz', 'success')
        return redirect(url_for('students.login'))
    return render_template('register.html', title='Kayıt Ol', form=form)

@students.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    return render_template('reset_request.html')

@students.route('/logout', methods=['GET', 'POST'])  
@login_required
def logout():
    logout_user()
    return redirect(url_for('students.login'))

@students.route('/unattendance', methods=['GET', 'POST'])
@login_required
def unattendance():
    form_get = GetUnattendancesForm()
    form_update = UpdateUnattendancesForm()

    lectures = Lecture.query.all()
    weeks = Weeks.query.all()

    form_update.lecture.choices = [(lecture.id, lecture.name) for lecture in lectures] 
    form_update.week.choices= [(week.id, week.week_name) for week in weeks]

    form_get.lecture.choices = [(lecture.id, lecture.name) for lecture in lectures]

    unattendances = None

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

    return render_template('unattendance.html', title='Devamsızlıklar', form_get=form_get, form_update = form_update, unattendances=unattendances)
    
@students.route('/delete/<int:id>', methods=['POST'])
def delete_unattendance(id):
    devamsizlik = Unattendance.query.options(joinedload(Unattendance.lecture)).get(id)

    if devamsizlik:
        db.session.delete(devamsizlik)
        db.session.commit()
        flash(f'Devamsızlık kaydı {devamsizlik.lecture.name} dersi için {devamsizlik.week_id}. haftadan silindi', 'info')
    return redirect(url_for('students.unattendance'))

@students.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profil', student=current_user)

@students.route('/add_lecture', methods=['GET', 'POST'])
@login_required
def add_lecture():
    form_add_lecture = AddLecture()

    if form_add_lecture.validate_on_submit():
        new_lecture = Lecture(name=form_add_lecture.lecture_name.data, code = form_add_lecture.lecture_code.data)
        db.session.add(new_lecture)
        db.session.commit()
        flash(f'{new_lecture.name} dersi {new_lecture.code} koduyla başarıyla eklendi', 'success')
        return redirect(url_for('students.unattendance'))
    
    return render_template('add_lecture.html', title='Ders Ekle', form_add = form_add_lecture)

#    if form.validate_on_submit():
#        student = Student.query.filter_by(email=form.email.data).first()
#        send_reset_email(student)
#        flash("Şifre sıfırlama linki gönderildi", "info")
#        return redirect(url_for("login"))

#   return render_template('reset_request.html', title='Şifreni Sıfırla', form=form)

#@students.route("/reset_password/<token>", methods=['GET', 'POST'])
#def reset_token(token):
#    student = Student.verify_reset_token(token)
#    if not student:
#        flash('Şifre sıfırlama linki geçersiz. Muhtemelen süresi dolmuş', 'danger')
#        return redirect(url_for('students.reset_request'))
    
#    form = ResetPasswordForm()
#    if form.validate_on_submit():
#            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
#            student.password = hashed_password
#            db.session.commit()
#            flash('Şifreniz başarıyla değiştirildi.', 'success')
#            return redirect(url_for('students.login'))
#    return render_template('reset_token.html', title='Şifreni Sıfırla', form=form)