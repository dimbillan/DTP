from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from dtp.models import Student, Announcement, Lecture
from dtp.admin.forms import AnnouncementForm
from dtp import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.is_admin or current_user.email == "admin@dtp.com":
        return render_template('admin.html', title='Admin Panel')
    
    else:
        return redirect(url_for('main.home'))
    
@admin.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    students = Student.query.all()
    return render_template('students.html', students = students)

@admin.route('/give_perm/<int:id>', methods=['POST'])
def give_perm(id):
    student = Student.query.get(id)

    if student:
        student.is_admin = 1
        db.session.commit()

        flash(f"ID'si {student.id} olan {student.name} adlı öğrenciye ADMIN yetkileri verildi", 'info')

    return redirect(url_for('admin.admin_panel'))

@admin.route('/take_perm/<int:id>', methods=['POST'])
def take_perm(id):
    student = Student.query.get(id)

    if student:
        student.is_admin = 0
        db.session.commit()

        flash(f"ID'si {student.id} olan {student.name} adlı öğrencinin ADMIN yetkileri kaldırıldı.", 'info')

    return redirect(url_for('admin.admin_panel'))


@admin.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

        flash(f"ID'si {student.id} olan {student.name} adlı öğrenci silindi.", 'info')

    return redirect(url_for('admin.students'))

@admin.route('/announcement', methods=['GET', 'POST'])
@login_required
def announcement():
    announcements = Announcement.query.all()

    return render_template('announcement.html', announcements = announcements[::-1])

@admin.route('/announcement/new', methods=['GET', 'POST'])
@login_required
def new_announcement():
    form_announcement = AnnouncementForm()

    if form_announcement.validate_on_submit():
        new_announcement = Announcement(author_id = current_user.id, title=form_announcement.title.data, content = form_announcement.content.data)
    
        db.session.add(new_announcement)
        db.session.commit()

        flash(f"Duyuru {form_announcement.title.data} başlığıyla eklendi", "success")

        return redirect(url_for('admin.announcement'))
    
    return render_template('add_announcement.html', title = "Duyuru Ekle", form_announcement = form_announcement)

@admin.route('/announcement/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_announcement(id):
    current_announcement = Announcement.query.get(id)
    form_announcement = AnnouncementForm(obj=current_announcement)
    

    if form_announcement.validate_on_submit():
        current_announcement.title = form_announcement.title.data
        current_announcement.content = form_announcement.content.data
        db.session.commit() 

        flash(f"{form_announcement.title.data} başlıklı duyuru güncellendi", "success")

        return redirect(url_for('admin.announcement'))
    
    return render_template('update_announcement.html', title = "Duyuru Ekle", form_announcement = form_announcement)

@admin.route('/announcement/delete/<int:id>', methods=['POST'])
def delete_announcement(id):
    announcement = Announcement.query.get(id)

    if announcement:
        db.session.delete(announcement)
        db.session.commit()

        flash(f"{announcement.title} başlıklı duyuru kaldırıldı.", 'info')

    return redirect(url_for('admin.admin_panel'))

@admin.route('/lectures', methods=['GET', 'POST'])
@login_required
def lectures():
    lectures = Lecture.query.all()

    return render_template('lectures.html', lectures = lectures)

@admin.route('/delete_lecture/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_lecture(id):
    lecture = Lecture.query.get_or_404(id)
    if not lecture:
        flash("Bir hata oluştu", "danger")
    else:
        db.session.delete(lecture)
        db.session.commit()
    return redirect(url_for('admin.lectures'))