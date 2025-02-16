from flask import url_for, redirect, flash, render_template
from flask_login import current_user, login_required

from dtp import db
from dtp.models import Student
from dtp.admin.forms import PrivilegeForm
from dtp.admin.utils import canReach

from . import admin

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