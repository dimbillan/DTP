from flask import url_for, redirect, flash, render_template, request, g
from flask_login import current_user, login_user, login_required, logout_user

from dtp import db, bcrypt, logger
from dtp.models import Student
from dtp.students.forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm
from dtp.students.utils import send_reset_email

from . import students

@students.before_request
def get_real_ip():
    g.real_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr

@students.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] zaten giriş yaptiği için anasayfaya yönlendirildi.") 

        return redirect(url_for('main.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] giriş yapti.") 
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{form.email.data}] hatalı giriş denemesi yapti.") 
            flash('Giriş Başarısız. Öğrenci numaranızı ve şifrenizi kontrol edin.', 'danger')

    return render_template('auth/login.html', title='Giriş Yap', form=form)

@students.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] zaten kaydolduğu için girişe yönlendirildi.")
        return redirect(url_for('main.home'))
    
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            student = Student(email=form.email.data, name=form.name.data, password=hashed_password)
            
            db.session.add(student)
            db.session.commit()

            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{form.email.data} - ({form.name.data})] kaydoldu.")
            flash('Hesabınız oluşturuldu. Artık giriş yapabilirsiniz', 'success')

            return redirect(url_for('students.login'))
        
        else:
            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{form.email.data} - {form.name.data}] kaydolma denemesi başarısız.")

    return render_template('auth/register.html', title='Kayıt Ol', form=form)

@students.route('/logout', methods=['GET', 'POST'])  
@login_required
def logout():
    logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] çikiş yapti.")
    logout_user()
    return redirect(url_for('students.login'))

@students.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    
    form = RequestResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        send_reset_email(student)
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{form.email.data}] şifre sıfırlama e-postası gönderildi.")
        flash('Şifre sıfırlama talimatları e-posta adresinize gönderildi.', 'info')
        return redirect(url_for('students.login'))
    
    return render_template('auth/reset_request.html', title='Şifre Sıfırlama', form=form)

@students.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    
    student = Student.verify_reset_token(token)
    if student is None:
        logger.warning(f"{request.method} - [IP: {g.real_ip}] - Geçersiz veya süresi dolmuş token ile şifre sıfırlama denemesi.")
        flash('Geçersiz ya da süresi dolmuş token.', 'warning')
        return redirect(url_for('students.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student.password = hashed_password
        db.session.commit()
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{student.email}({student.id})] şifresini başarıyla sıfırladı.")
        flash('Şifreniz başarıyla güncellendi! Artık giriş yapabilirsiniz.', 'success')
        return redirect(url_for('students.login'))
    
    return render_template('auth/reset_token.html', title='Şifre Sıfırlama', form=form)