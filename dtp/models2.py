from datetime import datetime
import pytz 
from dtp import db, login_manager
from sqlalchemy import event
from flask_login import UserMixin

@login_manager.user_loader
def load_user(student_id):
    return Student.query.get(int(student_id))

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Student ('{self.email}', '{self.name}', '{self.is_admin}')"
    
class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    code = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f"Lecture ('{self.name}', '{self.code}')"
    
class Weeks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_name = db.Column(db.String(64), nullable=False, unique=True)
    start_date = db.Column(db.String(64), nullable=False)
    end_date = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return f"Weeks ('{self.week_name}', '{self.start_date}', '{self.end_date}')"
    
class Unattendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lecture = db.relationship('Lecture', backref='unattendances')

    def __repr__(self):
        return f"Unattendances ('{self.student_id}', '{self.lecture_id}', '{self.week_id}')"
    
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="SET NULL"), nullable=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(64), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone("Europe/Istanbul")).astimezone(pytz.utc))
    author = db.relationship('Student', backref='announcements')
    def __repr__(self):
        return f"Announcement ('{self.author_id}', '{self.title}', '{self.content}', '{self.date_posted}')"
    
@event.listens_for(db.session, "before_commit")
def prevent_null_author(session):
    for instance in session.dirty:
        if isinstance(instance, Announcement) and instance.author_id is None:
            instance.author_id = -1