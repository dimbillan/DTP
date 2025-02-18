from flask import url_for, redirect, render_template , Response
from flask_login import login_required

from dtp.admin.utils import canReach

from . import admin

def read_logs():
    try:
        with open("debug.log", "r", encoding="utf-8", errors="ignore") as file:
            logs = file.readlines()
            logs.reverse()
            return logs
    except Exception as e:
        print(f"Log dosyası okunamadı: {str(e)}")

@admin.route("/logs")
@login_required
def logs():
    if canReach(100):
        logs = read_logs()
        return render_template("admin/logs.html", logs = logs)

    else:
        return redirect(url_for('main.home'))