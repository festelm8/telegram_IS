from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser, use_args

from src.schemas.web import teacher_create_post
from src.db import session, db
from src.db.models import Teacher
from . import bp_web

@bp_web.route('/teachers')
# @login_required
def teachers():
    teachers = Teacher.query.all();
    teacher_list = dict()
    if teachers:
        teacher_list = [{
            'id': teacher.id,
            'fio': teacher.name,
            'email': teacher.email
        } for teacher in teachers]
    return render_template('teachers.html', teacher_list=teacher_list)


@bp_web.route('/teachers/create', methods=['GET', 'POST'])
# @login_required
def teacher_create():
    if request.method == 'POST':
        data = parser.parse(teacher_create_post, request)
        teacher = Teacher()

        if data:
            for item in data.items():
                if item[0] == 'name':
                    teacher.name = item[1]
                if item[0] == 'email':
                    teacher.email = item[1]

            session.add(teacher)
            session.commit()
            return redirect(url_for('bp_web.teachers'))
    return render_template('teachers_edit.html')


@bp_web.route('/teachers/<teacher_id>', methods=['GET', 'POST'])
# @login_required
def teacher_edit(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return redirect(url_for('bp_web.teachers'))

    if request.method == 'POST':
        data = parser.parse(teacher_create_post, request)

        if data:
            for item in data.items():
                if item[0] == 'name':
                    teacher.name = item[1]
                if item[0] == 'email':
                    teacher.email = item[1]

            session.commit()
            return redirect(url_for('bp_web.teachers'))

    teacher = {
        'id': teacher_id,
        'fio': teacher.name,
        'email': teacher.email
    }
    return render_template('teachers_edit.html', teacher=teacher)

@bp_web.route('/teachers/<teacher_id>/delete')
# @login_required
def teacher_delete(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return redirect(url_for('bp_web.teachers'))
    if teacher.subjects.__len__() > 0:
        flash('Вы не можете удалить преподавателя, пока он закреплен за предметами!')
        return redirect(url_for('bp_web.teacher_edit', teacher_id=teacher_id))

    session.delete(teacher)
    session.commit()

    return redirect(url_for('bp_web.teachers'))
