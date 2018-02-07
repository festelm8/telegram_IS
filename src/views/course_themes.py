from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser, use_args

from src.schemas.web import course_theme_create_post, course_number_create_post, course_group_create_post
from src.db import session, db
from src.db.models import CourseTheme, CourseNumber, CourseGroup, Subject
from . import bp_web

@bp_web.route('/course_themes')
@login_required
def course_themes():
    course_themes = CourseTheme.query.all();
    course_themes_list = dict()
    if course_themes:
        course_themes_list = [{
            'id': course_theme.id,
            'name': course_theme.name
        } for course_theme in course_themes]
    return render_template('course_themes.html', course_themes_list=course_themes_list)


@bp_web.route('/course_themes/create', methods=['GET', 'POST'])
@login_required
def course_theme_create():
    if request.method == 'POST':
        data = parser.parse(course_theme_create_post, request)
        course_theme = CourseTheme()

        if data:
            for item in data.items():
                if item[0] == 'name':
                    course_theme.name = item[1]

            session.add(course_theme)
            session.commit()
            return redirect(url_for('bp_web.course_themes'))

    return render_template('course_themes_edit.html')


@bp_web.route('/course_themes/<course_theme_id>', methods=['GET', 'POST'])
@login_required
def course_theme_edit(course_theme_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_themes'))

    if request.method == 'POST':
        data = parser.parse(course_theme_create_post, request)

        if data:
            for item in data.items():
                if item[0] == 'name':
                    course_theme.name = item[1]

            session.commit()
            return redirect(url_for('bp_web.course_themes'))

    course_theme_data = {
        'id': course_theme.id,
        'name': course_theme.name,
        'course_numbers_list': dict()
    }
    if course_theme.course_number:
        course_theme_data['course_numbers_list'] = [{
            'id': course_number.id,
            'number': course_number.number
        } for course_number in course_theme.course_number]

    return render_template('course_themes_edit.html', course_theme_data=course_theme_data)


@bp_web.route('/course_themes/<course_theme_id>/delete')
@login_required
def course_theme_delete(course_theme_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_themes'))

    if course_theme.course_number.__len__() > 0:
        flash('Вы не можете удалить это направление подготовки пока у него есть активные курсы подготовки!')
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    session.delete(course_theme)
    session.commit()

    return redirect(url_for('bp_web.course_themes'))


@bp_web.route('/course_themes/<course_theme_id>/course_numbers/create', methods=['GET', 'POST'])
@login_required
def course_number_create(course_theme_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    reserved_courses = list()
    if course_theme.course_number:
        for course_number in course_theme.course_number:
            reserved_courses.append(course_number.number)

    subjects = Subject.query.all()
    subjects_list = dict()
    if subjects:
        subjects_list = [{
            'id': subject.id,
            'name': subject.name
        } for subject in subjects]


    if request.method == 'POST':
        data = parser.parse(course_number_create_post, request)
        course_number = CourseNumber()

        if data:
            for item in data.items():
                if item[0] == 'number':
                    course_number.number = int(item[1])
                if item[0] == 'subjects[]':
                    for subj in item[1]:
                        course_number_subject = Subject.query.get(subj)
                        if course_number_subject:
                            course_number.subjects.append(course_number_subject)
            course_number.course_theme = course_theme
            session.add(course_number)
            session.commit()

            return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    return render_template('course_numbers_edit.html', reserved_courses=reserved_courses, subjects_list=subjects_list)


@bp_web.route('/course_themes/<course_theme_id>/course_numbers/<course_number_id>', methods=['GET', 'POST'])
@login_required
def course_number_edit(course_theme_id, course_number_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    course_number = course_theme.course_number_lazy.filter_by(id=course_number_id).first()
    if not course_number:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    course_number_data = {
        'id': course_number.id,
        'course_theme_id': course_theme.id,
        'number': course_number.number,
        'reserved_subjects': list(),
        'reserved_groups': dict()
    }

    if course_number.subjects:
        reserved_subjects = course_number.subjects.all()
        if reserved_subjects:
            for reserved_subject in reserved_subjects:
                course_number_data['reserved_subjects'].append(reserved_subject.id)

    if course_number.course_group:
        course_number_data['reserved_groups'] = [{
            'id': reserved_group.id,
            'gid': reserved_group.gid
        } for reserved_group in course_number.course_group]

    reserved_courses = list()
    if course_theme.course_number:
        for course_number in course_theme.course_number:
            reserved_courses.append(course_number.number)

    subjects = Subject.query.all()
    subjects_list = dict()
    if subjects:
        subjects_list = [{
            'id': subject.id,
            'name': subject.name
        } for subject in subjects]


    if request.method == 'POST':
        data = parser.parse(course_number_create_post, request)

        if data:
            for item in data.items():
                if item[0] == 'number':
                    course_number.number = int(item[1])
                if item[0] == 'subjects[]':
                    reserved_subjects = course_number.subjects.all()
                    if reserved_subjects:
                        for reserved_subject in reserved_subjects:
                            course_number.subjects.remove(reserved_subject)
                    for subj in item[1]:
                        course_number_subject = Subject.query.get(subj)
                        if course_number_subject:
                            course_number.subjects.append(course_number_subject)

            session.commit()

            return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    return render_template('course_numbers_edit.html', course_number_data=course_number_data, reserved_courses=reserved_courses, subjects_list=subjects_list)


@bp_web.route('/course_themes/<course_theme_id>/course_numbers/<course_number_id>/delete')
@login_required
def course_number_delete(course_theme_id, course_number_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    course_number = course_theme.course_number_lazy.filter_by(id=course_number_id).first()
    if not course_number:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    if course_number.course_group.__len__() > 0 or course_number.subjects.count() > 0:
        flash('Вы не можете удалить этот номер курса, пока у него есть используемые группы или курс привязан к предметам!')
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    session.delete(course_theme)
    session.commit()

    return redirect(url_for('bp_web.course_themes'))


@bp_web.route('/course_themes/<course_theme_id>/course_numbers/<course_number_id>/create_group', methods=['POST'])
@login_required
def course_group_create(course_theme_id, course_number_id):
    course_theme = CourseTheme.query.get(course_theme_id)
    if not course_theme:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))

    course_number = course_theme.course_number_lazy.filter_by(id=course_number_id).first()
    if not course_number:
        return redirect(url_for('bp_web.course_theme_edit', course_theme_id=course_theme_id))


    course_group = CourseGroup()
    data = parser.parse(course_group_create_post, request)


    if data:
        for item in data.items():
            if item[0] == 'gid':
                course_group.gid = int(item[1])

        course_group.course_number = course_number
        session.add(course_group)
        session.commit()

    return redirect(url_for('bp_web.course_number_edit', course_theme_id=course_theme_id, course_number_id=course_number_id))


@bp_web.route('/course_themes/<course_theme_id>/course_numbers/<course_number_id>/<course_group_id>')
@login_required
def course_group_delete(course_theme_id, course_number_id, course_group_id):
    course_group = CourseGroup.query.get(course_group_id)
    if not course_group:
        return redirect(url_for('bp_web.course_number_edit', course_theme_id=course_theme_id, course_number_id=course_number_id))

    if course_group.class_schedule.count() > 0:
        flash('Вы не можете удалить эту группу пока у она числиться в расписании!')
        return redirect(url_for('bp_web.course_number_edit', course_theme_id=course_theme_id, course_number_id=course_number_id))

    session.delete(course_group)
    session.commit()

    return redirect(url_for('bp_web.course_number_edit', course_theme_id=course_theme_id, course_number_id=course_number_id))

