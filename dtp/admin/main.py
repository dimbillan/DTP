from flask import render_template, redirect, url_for

from flask_login import login_required

from dtp.admin.utils import canReach

from . import admin

@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if canReach(10):
        return render_template('admin/admin.html', title='Admin Panel')
    
    else:
        return redirect(url_for('main.home'))