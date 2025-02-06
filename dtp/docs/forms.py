from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from werkzeug.utils import secure_filename

class DocsForm(FlaskForm):
    
    docs_file = FileField('Belge Yükle', validators=[FileAllowed(['jpg','png','jpeg']), InputRequired()])
    
    docs_lecture = SelectField('Docs Lecture', choices=[], validators=[InputRequired()])

    submit = SubmitField('Ekle')

class DocsFormQuery(FlaskForm):
    
    docs_lecture_query = SelectField('Docs Lecture', choices=[], validators=[InputRequired()])

    submit = SubmitField('Sorgula')    