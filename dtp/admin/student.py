from flask import url_for, redirect, flash, render_template, current_app
from flask_login import current_user, login_required
from functools import wraps

from dtp import db
from dtp.models import Student
from dtp.admin.forms import PrivilegeForm
from dtp.admin.utils import canReach

from . import admin

def admin_required(min_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not canReach(min_level):
                flash("Bu işlem için yeterli yetkiniz yok.", "danger")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@admin.route('/students', methods=['GET', 'POST'])
@login_required
@admin_required(100)
def students():
    try:
        students = Student.query.all()
        return render_template('admin/students.html', students=students)
    except Exception as e:
        current_app.logger.error(f"Öğrenci listesi görüntüleme hatası: {str(e)}")
        flash("Bir hata oluştu.", "danger")
        return redirect(url_for('main.home'))

@admin.route('/change_perm/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required(100)
def change_perm(id):
    try:
        student = Student.query.get_or_404(id)
        form_change = PrivilegeForm()

        if form_change.validate_on_submit():
            # İşlem öncesi tekrar yetki kontrolü
            if not canReach(100):
                flash("Bu işlem için yeterli yetkiniz yok.", "danger")
                return redirect(url_for('main.home'))

            if current_user.is_admin < form_change.level.data:
                flash("Kendi yetki seviyenizden daha yüksek bir yetki veremezsiniz.", "danger")
    
            elif current_user.is_admin < student.is_admin:
                flash(f"{student.name} adlı öğrencinin mevcut yetkisi, sizin yetkinizden daha yüksek.", "danger")

            elif form_change.level.data < 1 or form_change.level.data > 100:
                flash(f"Yetki seviyesi 1-100 arasında olmalıdır", "danger")
            else:
                student.is_admin = form_change.level.data
                try:
                    db.session.commit()
                    flash(f"{student.name} (ID: {student.id}) adlı öğrencinin yetki seviyesi {student.is_admin} olarak güncellenmiştir.", 'info')
                    return redirect(url_for('admin.admin_panel'))
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(f"Yetki güncelleme hatası: {str(e)}")
                    flash("Yetki güncellenirken bir hata oluştu.", "danger")
        
        return render_template("admin/change_perm.html", form_change=form_change, student=student)
    
    except Exception as e:
        current_app.logger.error(f"Yetki değiştirme sayfası hatası: {str(e)}")
        flash("Bir hata oluştu.", "danger")
        return redirect(url_for('main.home'))

@admin.route('/delete_student/<int:id>', methods=['POST'])
@login_required
@admin_required(100)
def delete_student(id):
    try:
        student = Student.query.get_or_404(id)

        # İşlem öncesi tekrar yetki kontrolü
        if not canReach(100):
            flash("Bu işlem için yeterli yetkiniz yok.", "danger")
            return redirect(url_for('main.home'))

        if current_user.is_admin < student.is_admin:
            flash(f"{student.name} adlı öğrencinin mevcut yetkisi, sizin yetkinizden daha yüksek.", "danger")
        else:
            try:
                db.session.delete(student)
                db.session.commit()
                flash(f"ID'si {student.id} olan {student.name} adlı öğrenci silindi.", 'info')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Öğrenci silme hatası: {str(e)}")
                flash("Öğrenci silinirken bir hata oluştu.", "danger")

        return redirect(url_for('admin.students'))
    
    except Exception as e:
        current_app.logger.error(f"Öğrenci silme işlemi hatası: {str(e)}")
        flash("Bir hata oluştu.", "danger")
        return redirect(url_for('main.home'))