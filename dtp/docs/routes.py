import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, request, g
from flask_login import login_required, current_user

from dtp import logger
from dtp.docs.forms import DocsForm, DocsFormQuery
from dtp.models import Lecture

docs = Blueprint('docs', __name__)

@docs.before_request
def get_real_ip():
    g.real_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr

@docs.route('/docs', methods=['GET', 'POST'])
@login_required
def docs_list():

    lectures = Lecture.query.all()

    form_docs = DocsForm()
    form_docs.docs_lecture.choices = [(lecture.id, lecture.name) for lecture in lectures]

    form_docs_q = DocsFormQuery()
    form_docs_q.docs_lecture_query.choices = [(lecture.id, lecture.name) for lecture in lectures]

    logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] belge sayfasinda.")

    if form_docs.validate_on_submit():
        docs_lecture = form_docs.docs_lecture.data
        docs_file = form_docs.docs_file.data

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_extension = os.path.splitext(docs_file.filename)[1]
        new_filename = f"{docs_lecture}_{timestamp}{file_extension}"

        docs_file.save(os.path.join("dtp/static/docs", new_filename))

        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] {new_filename} adli {docs_lecture} numarali ders için belge yükledi.")
        flash('Belge başariyla yüklendi', 'success')
        
        return redirect('/docs')
    
    if form_docs_q.validate_on_submit():
        docs_lecture = form_docs_q.docs_lecture_query.data
        docs = [f for f in os.listdir("dtp/static/docs") if f.endswith(('.jpg', '.jpeg', '.png')) and f.startswith(docs_lecture)]

        logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] {docs_lecture} numarali dersin belgelerini sorguladi.")

        return render_template('students/docs.html', title='Belgeler', form_docs=form_docs, form_query = form_docs_q, docs=docs)
    
    docs = [f for f in os.listdir("dtp/static/docs") if f.endswith(('.jpg', '.jpeg', '.png'))]
    return render_template('students/docs.html', title='Belgeler', form_docs=form_docs, form_query = form_docs_q, docs=docs)

@docs.route('/docs/delete/<string:filename>', methods=['GET', 'POST'])
@login_required
def delete_file(filename):
    if current_user.is_admin > 50:
        file_path = os.path.join("dtp","static","docs",filename)
        
        if os.path.exists(file_path):

            try:
                os.remove(file_path)
                logger.info(f"{request.method} - [IP: {g.real_ip}] - [{current_user.name}({current_user.id})] {filename} adli belgeyi sildi.") 
                flash(f"{filename} başarıyla silindi.", "success")
            except Exception as e:
                flash(f"Belge silinirken bir hata oluştu: {str(e)}", "danger")

        else:
            flash("Belge bulunamadı.", "warning")

    else:
        flash("Bu işlemi gerçekleştirmek için yetkiniz yok.", "danger")
    
    return redirect('/docs')

