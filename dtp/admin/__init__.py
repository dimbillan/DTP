from flask import Blueprint

from dtp.admin.utils import *

admin = Blueprint('admin', __name__, url_prefix='/admin')

from . import announcement, lecture, main, student