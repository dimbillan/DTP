import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

from dtp.config import Config

app = Flask(__name__)

app.config.from_object(Config)
print(Config.SQLALCHEMY_DATABASE_URI)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'students.login'
login_manager.login_message_category = 'info'

from dtp.admin.routes import admin
from dtp.docs.routes import docs
from dtp.main.routes import main
from dtp.students.routes import students

app.register_blueprint(admin)
app.register_blueprint(docs)
app.register_blueprint(main)
app.register_blueprint(students)

from dtp.models import Student, Lecture, Unattendance

@app.context_processor
def inject_to_base():

    folder_path = os.path.join('dtp', 'static', 'docs')

    file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    total_students = db.session.query(Student).count()
    total_lectures = db.session.query(Lecture).count()
    total_unattendances = db.session.query(Unattendance).count()

    return {'total_students': total_students,
            'total_lectures': total_lectures,
            'total_unattendances': total_unattendances,
            'total_files': file_count}
