from flask import url_for, redirect, render_template, Response, request, current_app
from flask_login import login_required
from math import ceil
import os

from dtp.admin.utils import canReach

from . import admin

def read_logs(page=1, per_page=50):
    try:
        # Güvenli bir şekilde log dosyası yolunu oluştur
        log_path = os.path.abspath(os.path.join(current_app.root_path, '..', 'debug.log'))
        
        # Path traversal kontrolü
        if not log_path.startswith(os.path.abspath(os.path.join(current_app.root_path, '..'))):
            raise SecurityError("Geçersiz dosya yolu")
            
        if not os.path.exists(log_path):
            return [], 0, 1

        with open(log_path, "r", encoding="utf-8", errors="ignore") as file:
            all_logs = file.readlines()
            all_logs.reverse()
            
            total_logs = len(all_logs)
            total_pages = ceil(total_logs / per_page)
            
            page = max(1, min(page, total_pages))
            
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            page_logs = all_logs[start_idx:end_idx]
            
            return page_logs, total_pages, page
    except Exception as e:
        current_app.logger.error(f"Log okuma hatası: {str(e)}")
        return [], 0, 1

class SecurityError(Exception):
    pass

@admin.route("/logs")
@login_required
def logs():
    if not canReach(100):
        return redirect(url_for('main.home'))
    
    try:
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
        logs, total_pages, current_page = read_logs(page=page)
        
        return render_template(
            "admin/logs.html",
            logs=logs,
            total_pages=total_pages,
            current_page=current_page,
            max=max,
            min=min
        )
    except Exception as e:
        current_app.logger.error(f"Logs sayfası hatası: {str(e)}")
        return redirect(url_for('main.home'))