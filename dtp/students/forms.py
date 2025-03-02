from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, EmailField
from wtforms.validators import Length, InputRequired, EqualTo, ValidationError, Email, DataRequired

from dtp.models import Student, Lecture, Unattendance

class RegisterForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired(), Email()], render_kw={"placeholder": "E-Posta"})
    
    name = StringField(validators=[
                            InputRequired(), Length(min=3, max=64)], render_kw={"placeholder": "Ad Soyad"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=6, max=64)], render_kw={"placeholder": "Şifre"})
    
    confirm_password = PasswordField(validators=[
                            InputRequired(), EqualTo('password')], render_kw={"placeholder": "Şifreyi Tekrar Yaz"})
    
    submit = SubmitField('Kayıt Ol')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Bu e-posta ile daha önce kayıt olunmuş. Lütfen başka bir e-posta seçin')

class LoginForm(FlaskForm):
    email = EmailField(validators=[
                           InputRequired(), Email() ], render_kw={"placeholder": "E-Posta"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=6, max=64)], render_kw={"placeholder": "Şifre"})

    submit = SubmitField('Giriş Yap')

class RequestResetForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()], render_kw={"placeholder": "E-Posta"})
    submit = SubmitField('Şifre Sıfırlama İsteği Gönder')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student is None:
            raise ValidationError('Bu e-posta adresi ile kayıtlı bir hesap bulunamadı.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Yeni Şifre"})
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Yeni Şifreyi Onayla"})
    submit = SubmitField('Şifreyi Sıfırla')

class UpdateUnattendancesForm(FlaskForm):
    lecture = SelectField('Lecture', choices=[], validators=[InputRequired()])
    
    week = SelectField('Week', choices=[])
    
    submit = SubmitField('Ekle')

    def validate_attendance(self, week):
        attendance = Unattendance.query.filter_by(week_id=week.data).first()
        if attendance:
            raise ValidationError('Bu numara daha önce alınmış. Lütfen başka bir numara seçin')
        
class GetUnattendancesForm(FlaskForm):

    lecture = SelectField('Lecture', choices=[], validators=[InputRequired()])
    
    submit = SubmitField('Sorgula')