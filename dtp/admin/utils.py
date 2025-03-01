from flask import redirect, url_for
from flask_login import current_user

def canReach(required_level):
    # Yetki seviyesi kontrolü
    if not isinstance(required_level, int) or required_level < 1:
        return False
    
    # Admin yetkisi kontrolü
    if not hasattr(current_user, 'is_admin') or not isinstance(current_user.is_admin, int):
        return False
    
    return current_user.is_admin >= required_level