from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, InputRequired, EqualTo, ValidationError, Email

from dtp.models import Announcement

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