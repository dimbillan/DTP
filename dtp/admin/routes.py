from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from dtp.models import Student, Announcement, Lecture
from dtp.admin.forms import AnnouncementForm, AddLecture, PrivilegeForm
from dtp.admin.utils import canReach

from dtp import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if canReach(10):
        return render_template('admin/admin.html', title='Admin Panel')
    
    else:
        return redirect(url_for('main.home'))
    
@admin.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    if canReach(100):
        students = Student.query.all()
        return render_template('admin/students.html', students = students)
    else:
        return redirect(url_for('main.home'))

@admin.route('/change_perm/<int:id>', methods=['GET', 'POST'])
@login_required
def change_perm(id):
    if canReach(100):
        student = Student.query.get(id)
        form_change = PrivilegeForm()

        if form_change.validate_on_submit():
            if student:
                if current_user.is_admin < form_change.level.data:
                    flash("Kendi yetki seviyenizden daha yüksek bir yetki veremezsiniz. Lütfen geçerli bir yetki seviyesi seçin.", "danger")
        
                elif current_user.is_admin < student.is_admin:
                    flash(f"{student.name} adlı öğrencinin mevcut yetkisi, sizin yetkinizden daha yüksek. Bu yüzden değişiklik yapılamaz.", "danger")

                elif form_change.level.data < 1:
                    flash(f"Yetki seviyesi 1'den küçük olamaz", "danger")
                else:
                    student.is_admin = form_change.level.data
                    db.session.commit()

                    flash(f"{student.name} (ID: {student.id}) adlı öğrencinin yetki seviyesi {student.is_admin} olarak güncellenmiştir.", 'info')
                    return redirect(url_for('admin.admin_panel'))
            
        return render_template("admin/change_perm.html", form_change=form_change, student=student)
    
    else:
        flash("Bu işlemi gerçekleştirmek için gerekli yetkiye sahip değilsiniz.", "danger")
        return redirect(url_for('main.home'))

@admin.route('/delete_student/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    if canReach(100):
        student = Student.query.get(id)

        if student:
            if current_user.is_admin < student.is_admin:
                flash(f"{student.name} adlı öğrencinin mevcut yetkisi, sizin yetkinizden daha yüksek. Bu yüzden değişiklik yapılamaz.", "danger")

            else:
                db.session.delete(student)
                db.session.commit()
                flash(f"ID'si {student.id} olan {student.name} adlı öğrenci silindi.", 'info')

        return redirect(url_for('admin.students'))
    
    else:
        return redirect(url_for('main.home'))
    
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
    
@admin.route('/lectures', methods=['GET', 'POST'])
@login_required
def lectures():
    if canReach(10):
        lectures = Lecture.query.all()

        return render_template('admin/lectures.html', lectures = lectures)
    
    else:
        return redirect(url_for('main.home'))
    
@admin.route('/delete_lecture/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_lecture(id):
    if canReach(50):
        lecture = Lecture.query.get_or_404(id)
        if not lecture:
            flash("Bir hata oluştu", "danger")
        else:
            db.session.delete(lecture)
            db.session.commit()

            flash(f"{lecture.name} dersi silindi.", "info")

        return redirect(url_for('admin.lectures'))
    
    else:
        return redirect(url_for('main.home'))


@admin.route('/add_lecture', methods=['GET', 'POST'])
@login_required
def add_lecture():
    if canReach(50):
        form_add = AddLecture()
        if form_add.validate_on_submit():
            new_lecture = Lecture(name=form_add.lecture_name.data, code = form_add.lecture_code.data)
            
            db.session.add(new_lecture)
            db.session.commit()
            
            flash(f"{form_add.lecture_name.data} dersi {form_add.lecture_code.data} koduyla eklendi.", "success")

            return redirect(url_for("admin.lectures"))

        return render_template("admin/add_lecture.html", form_add=form_add)
    
    else:
        return redirect(url_for('main.home'))