from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import Length, InputRequired, EqualTo, ValidationError, Email

from dtp.models import Announcement, Lecture

class AnnouncementForm(FlaskForm):
    title = StringField(validators=[
                            InputRequired(), Length(min=2, max=128)], render_kw={"placeholder": "Başlık"})
    
    content = TextAreaField(validators=[
                            InputRequired(), Length(min=2, max=1024)], render_kw={"placeholder": "İçerik"})
    
    submit = SubmitField('Duyuru Ekle/Güncelle')

    def validate_title(self, title):
        announcement = Announcement.query.filter_by(title=title.data).first()
        if announcement:
            raise ValidationError('Bu başlık ile daha önce duyuru yapılmış. Lütfen başka başlık seçin')
        
class PrivilegeForm(FlaskForm):
    level = IntegerField(validators=[
                                        InputRequired()], render_kw={"placeholder": "Seviye"})
    
    submit = SubmitField("Yetkilendir")

class AddLecture(FlaskForm):
    lecture_name = StringField (validators=[InputRequired(), Length(min=1, max=64)], render_kw={"placeholder": "Dersin Adı"})

    lecture_code = StringField (validators=[InputRequired(), Length(min=1, max=64)], render_kw={"placeholder": "Ders Kodu (Örneğin: OMB 1001)"})

    submit = SubmitField('Ekle')

    def validate_lecture_code(self, lecture_code):
        lecture = Lecture.query.filter_by(code=lecture_code.data).first()
        if lecture:
            raise ValidationError('Bu ders koduyla daha önce ders eklenmiş. Lütfen kodu kontrol edin.')