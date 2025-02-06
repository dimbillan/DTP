import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from dtp.docs.forms import DocsForm, DocsFormQuery
from dtp.models import Lecture
from dtp.docs.utils import isAllowed

docs = Blueprint('docs', __name__)


@docs.route('/docs', methods=['GET', 'POST'])
@login_required
def docs_list():

    lectures = Lecture.query.all()
    form_docs = DocsForm()
    form_docs.docs_lecture.choices = [(lecture.id, lecture.name) for lecture in lectures]
    form_docs_q = DocsFormQuery()
    form_docs_q.docs_lecture_query.choices = [(lecture.id, lecture.name) for lecture in lectures]
        
    if form_docs.validate_on_submit():
        docs_lecture = form_docs.docs_lecture.data
        docs_file = form_docs.docs_file.data

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_extension = os.path.splitext(docs_file.filename)[1]
        new_filename = f"{docs_lecture}_{timestamp}{file_extension}"

        docs_file.save(os.path.join("dtp/static/docs", new_filename))

        flash('Dosya başarıyla yüklendi', 'success')
        
        return redirect('/docs')
    
    if form_docs_q.validate_on_submit():
        docs_lecture = form_docs_q.docs_lecture_query.data
        docs = [f for f in os.listdir("dtp/static/docs") if f.endswith(('.jpg', '.jpeg', '.png')) and f.startswith(docs_lecture)]
        return render_template('docs.html', title='Belgeler', form_docs=form_docs, form_query = form_docs_q, docs=docs)
    return render_template('docs.html', title='Belgeler', form_docs=form_docs, form_query = form_docs_q)

@docs.route('/docs/delete/<string:filename>', methods=['GET', 'POST'])
@login_required
def delete_file(filename):
    if current_user.is_admin:
        file_path = os.path.join("dtp","static","docs",filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                flash(f"{filename} başarıyla silindi.", "success")
            except Exception as e:
                flash(f"Dosya silinirken bir hata oluştu: {str(e)}", "danger")
        else:
            flash("Dosya bulunamadı.", "warning")
    else:
        flash("Bu işlemi gerçekleştirmek için yetkiniz yok.", "danger")
    
    return redirect('/docs')

