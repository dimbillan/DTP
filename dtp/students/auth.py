from flask import url_for, redirect, flash, render_template, request, g
from flask_login import current_user, login_user, login_required, logout_user

from dtp import db, bcrypt, logger
from dtp.models import Student
from dtp.students.forms import LoginForm, RegisterForm

from . import students

@students.before_request
def get_real_ip():
    g.real_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr

@students.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] zaten giriş yaptığı için anasayfaya yönlendirildi.") 

        return redirect(url_for('main.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] giriş yaptı.") 
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            logger.info(f"{request.method} - [IP: {g.real_ip}] - [{form.email.data}] hatalı giriş denemesi yaptı.") 
            flash('Giriş Başarısız. Öğrenci numaranızı ve şifrenizi kontrol edin.', 'danger')

    return render_template('auth/login.html', title='Giriş Yap', form=form)

@students.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] zaten kaydolduğu yaptığı için girişe yönlendirildi.")
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
    logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] çıkış yaptı.")
    logout_user()
    return redirect(url_for('students.login'))

@students.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    return render_template('auth/reset_request.html')


#    if form.validate_on_submit():
#        student = Student.query.filter_by(email=form.email.data).first()
#        send_reset_email(student)
#        flash("Şifre sıfırlama linki gönderildi", "info")
#        return redirect(url_for("login"))

#   return render_template('auth/reset_request.html', title='Şifreni Sıfırla', form=form)

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
#    return render_template('auth/reset_token.html', title='Şifreni Sıfırla', form=form)