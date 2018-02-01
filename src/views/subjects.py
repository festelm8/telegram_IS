from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser, use_args

from src.schemas.web import subects_create_post
from src.db import session, db
from src.db.models import Teacher, Subject
from . import bp_web

@bp_web.route('/subjects')
# @login_required
def subjects():
    subjects = Subject.query.all();
    subject_list = dict()
    if subjects:
        subject_list = [{
            'id': subject.id,
            'name': subject.name,
            'desc': subject.desc,
            'teacher': subject.teacher.name
        } for subject in subjects]
    return render_template('subjects.html', subject_list=subject_list)


@bp_web.route('/subjects/create', methods=['GET', 'POST'])
# @login_required
def subject_create():
    teachers = Teacher.query.all();
    teacher_list = dict()
    if teachers:
        teacher_list = [{
            'id': teacher.id,
            'fio': teacher.name
        } for teacher in teachers]

    if request.method == 'POST':
        data = parser.parse(subects_create_post, request)
        subject = Subject()

        if data:
            for item in data.items():
                if item[0] == 'name':
                    subject.name = item[1]
                if item[0] == 'desc':
                    subject.desc = item[1]
                if item[0] == 'teacher_id':
                    teacher = Teacher.query.get(item[1])
                    if not teacher:
                        return redirect(url_for('bp_web.subjects'))
                    subject.teacher = teacher

            session.add(subject)
            session.commit()
            return redirect(url_for('bp_web.subjects'))
    return render_template('subjects_edit.html', teacher_list=teacher_list)


@bp_web.route('/subjects/<subject_id>', methods=['GET', 'POST'])
# @login_required
def subject_edit(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for('bp_web.subjects'))

    teachers = Teacher.query.all();
    teacher_list = dict()
    if teachers:
        teacher_list = [{
            'id': teacher.id,
            'fio': teacher.name
        } for teacher in teachers]

    if request.method == 'POST':
        data = parser.parse(subects_create_post, request)

        if data:
            for item in data.items():
                if item[0] == 'name':
                    subject.name = item[1]
                if item[0] == 'desc':
                    subject.desc = item[1]
                if item[0] == 'teacher_id':
                    teacher = Teacher.query.get(item[1])
                    if not teacher:
                        return redirect(url_for('bp_web.subjects'))
                    subject.teacher = teacher

            session.commit()
            return redirect(url_for('bp_web.subjects'))

    subject = {
        'id': subject_id,
        'name': subject.name,
        'desc': subject.desc,
        'teacher_id': subject.teacher.id
    }
    return render_template('subjects_edit.html', subject=subject, teacher_list=teacher_list)

@bp_web.route('/subjects/<subject_id>/delete')
# @login_required
def subject_delete(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return redirect(url_for('bp_web.subjects'))
    if subject.lessons.__len__() > 0 or subject.course_subscribed.count() > 0:
        flash('Вы не можете удалить предмет, пока на него подписаны курсы или он присутствует в расписании!')
        return redirect(url_for('bp_web.subject_edit', subject_id=subject_id))

    session.delete(subject)
    session.commit()

    return redirect(url_for('bp_web.subjects'))
