from flask import url_for, redirect, flash, render_template
from flask_login import login_required, current_user

from dtp import db
from dtp.models import Announcement
from dtp.admin.forms import AnnouncementForm
from dtp.admin.utils import canReach

from . import admin

@admin.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement():
    if canReach(10):
        announcements = Announcement.query.all()
        return render_template('admin/announcement.html', announcements = announcements[::-1])
    
    else:
        return redirect(url_for('main.home'))

@admin.route('/announcement/new', methods=['GET', 'POST'])
@login_required
def new_announcement():
    if canReach(20):
        form_announcement = AnnouncementForm()

        if form_announcement.validate_on_submit():
            new_announcement = Announcement(author_id = current_user.id, title=form_announcement.title.data, content = form_announcement.content.data)
        
            db.session.add(new_announcement)
            db.session.commit()

            flash(f"Duyuru {form_announcement.title.data} başlığıyla eklendi", "success")

            return redirect(url_for('admin.new_announcement'))
        
        return render_template('admin/add_announcement.html', title = "Duyuru Ekle", form_announcement = form_announcement)
    
    else:
        return redirect(url_for('main.home'))
    
@admin.route('/announcement/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_announcement(id):
    if canReach(10):
        current_announcement = Announcement.query.get(id)
        form_announcement = AnnouncementForm(obj=current_announcement)
        

        if form_announcement.validate_on_submit():
            current_announcement.title = form_announcement.title.data
            current_announcement.content = form_announcement.content.data
            db.session.commit() 

            flash(f"{form_announcement.title.data} başlıklı duyuru güncellendi", "success")

            return redirect(url_for('admin.new_announcement'))
        
        return render_template('admin/update_announcement.html', title = "Duyuru Ekle", form_announcement = form_announcement)
    else:
        return redirect(url_for('main.home'))

@admin.route('/announcement/delete/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    if canReach(20):
        announcement = Announcement.query.get(id)

        if announcement:
            db.session.delete(announcement)
            db.session.commit()

            flash(f"{announcement.title} başlıklı duyuru kaldırıldı.", 'info')

        return redirect(url_for('admin.new_announcement'))
    
    else:
        return redirect(url_for('main.home'))