from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import Length, InputRequired, EqualTo, ValidationError, Email, NumberRange
from flask import current_app

from dtp.models import Announcement, Lecture

class AnnouncementForm(FlaskForm):
    class Meta:
        csrf = True  # CSRF koruması aktif

    title = StringField(validators=[
                            InputRequired(message="Başlık gerekli"), 
                            Length(min=2, max=128, message="Başlık 2-128 karakter arasında olmalı")
                        ], render_kw={"placeholder": "Başlık"})
    
    content = TextAreaField(validators=[
                            InputRequired(message="İçerik gerekli"), 
                            Length(min=2, max=1024, message="İçerik 2-1024 karakter arasında olmalı")
                        ], render_kw={"placeholder": "İçerik"})
    
    submit = SubmitField('Duyuru Ekle/Güncelle')

    def validate_title(self, title):
        if not title.data or not isinstance(title.data, str):
            raise ValidationError('Geçersiz başlık formatı')
        
        # XSS koruması için özel karakterleri kontrol et
        if any(char in title.data for char in ['<', '>', '"', "'", ';']):
            raise ValidationError('Başlık özel karakterler içeremez')
            
        announcement = Announcement.query.filter_by(title=title.data).first()
        if announcement:
            raise ValidationError('Bu başlık ile daha önce duyuru yapılmış. Lütfen başka başlık seçin')
        
class PrivilegeForm(FlaskForm):
    class Meta:
        csrf = True  # CSRF koruması aktif

    level = IntegerField(validators=[
                            InputRequired(message="Seviye gerekli"),
                            NumberRange(min=1, max=100, message="Seviye 1-100 arasında olmalı")
                        ], render_kw={"placeholder": "Seviye"})
    
    submit = SubmitField("Yetkilendir")

class AddLecture(FlaskForm):
    class Meta:
        csrf = True  # CSRF koruması aktif

    lecture_name = StringField(validators=[
                                InputRequired(message="Ders adı gerekli"), 
                                Length(min=1, max=64, message="Ders adı 1-64 karakter arasında olmalı")
                            ], render_kw={"placeholder": "Dersin Adı"})

    lecture_code = StringField(validators=[
                                InputRequired(message="Ders kodu gerekli"), 
                                Length(min=1, max=64, message="Ders kodu 1-64 karakter arasında olmalı")
                            ], render_kw={"placeholder": "Ders Kodu (Örneğin: OMB 1001)"})

    submit = SubmitField('Ekle')

    def validate_lecture_code(self, lecture_code):
        if not lecture_code.data or not isinstance(lecture_code.data, str):
            raise ValidationError('Geçersiz ders kodu formatı')
        
        # Ders kodu formatını kontrol et (örn: XXX 1234)
        import re
        if not re.match(r'^[A-Z]{3}\s\d{4}$', lecture_code.data):
            raise ValidationError('Ders kodu formatı geçersiz. Örnek format: XXX 1234')
            
        lecture = Lecture.query.filter_by(code=lecture_code.data).first()
        if lecture:
            raise ValidationError('Bu ders koduyla daha önce ders eklenmiş. Lütfen kodu kontrol edin.')