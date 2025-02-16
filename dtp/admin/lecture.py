from flask import url_for, redirect, flash, render_template
from flask_login import login_required

from dtp import db
from dtp.models import Lecture
from dtp.admin.forms import AddLecture
from dtp.admin.utils import canReach

from . import admin

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