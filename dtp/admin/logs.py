from flask import url_for, redirect, render_template, Response, request
from flask_login import login_required
from math import ceil

from dtp.admin.utils import canReach

from . import admin

def read_logs(page=1, per_page=50):
    try:
        with open("debug.log", "r", encoding="utf-8", errors="ignore") as file:
            all_logs = file.readlines()
            all_logs.reverse()
            
            # Toplam sayfa sayısını hesapla
            total_logs = len(all_logs)
            total_pages = ceil(total_logs / per_page)
            
            # Geçerli sayfa kontrolü
            page = max(1, min(page, total_pages))
            
            # Sayfa için log aralığını hesapla
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            # Sayfa için logları al
            page_logs = all_logs[start_idx:end_idx]
            
            return page_logs, total_pages, page
    except Exception as e:
        print(f"Log dosyası okunamadı: {str(e)}")
        return [], 0, 1

@admin.route("/logs")
@login_required
def logs():
    if canReach(100):
        page = request.args.get('page', 1, type=int)
        logs, total_pages, current_page = read_logs(page=page)
        
        return render_template(
            "admin/logs.html",
            logs=logs,
            total_pages=total_pages,
            current_page=current_page,
            max=max,
            min=min
        )
    else:
        return redirect(url_for('main.home'))