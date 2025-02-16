from flask import Blueprint

from dtp.students.utils import *

students = Blueprint('students', __name__)

from . import auth, profile, unattendance