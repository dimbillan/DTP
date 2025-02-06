from flask import Blueprint, render_template
from dtp.models import Announcement

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    announcements = Announcement.query.all()
    return render_template('home.html', title='DTP', announcements=announcements)