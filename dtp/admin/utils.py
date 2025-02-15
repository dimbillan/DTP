from flask import redirect, url_for
from flask_login import current_user

def canReach(required_level):
    if current_user.is_admin >= required_level:
        return True
    elif current_user.is_admin < required_level:
        return False
    else:
        return False