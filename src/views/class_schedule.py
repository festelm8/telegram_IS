from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser, use_args

from src.schemas.web import class_schedule_show_post, class_schedule_edit_post
from src.db import session, db
from src.db.models import CourseTheme, ClassSchedule, CourseGroup, Subject
from . import bp_web

@bp_web.route('/class_schedule', methods=['GET', 'POST'])
@login_required
def class_schedule():
    if request.method == 'POST':
        data = parser.parse(class_schedule_show_post, request)
        course_group = CourseGroup.query.get(data.get('gid'))
        if course_group:
            subjects = Subject.query.all()
            subjects_list = dict()
            if subjects:
                subjects_list = [{
                    'id': subject.id,
                    'name': subject.name
                } for subject in subjects]

            schedules = {
                'dows' : [
                    {'name': 'Понедельник', 'id': 'mon'},
                    {'name': 'Вторник', 'id': 'tue'},
                    {'name': 'Среда', 'id': 'wed'},
                    {'name': 'Четверг', 'id': 'thu'},
                    {'name': 'Пятница', 'id': 'fri'},
                    {'name': 'Суббота', 'id': 'sat'}
                ],
                'less_seq': [1,2,3,4,5,6,7,8]
            }

            current_schedule = dict()
            class_schedules = course_group.class_schedule.all()
            if class_schedules:
                for class_schedule in class_schedules:
                    current_schedule[class_schedule.dow+'_'+str(class_schedule.seq)+'_class'] = class_schedule.classroom
                    current_schedule[class_schedule.dow+'_'+str(class_schedule.seq)+'_subj'] = class_schedule.subject.id

            return render_template('class_schedule_edit.html', subjects_list=subjects_list, schedules=schedules, current_schedule=current_schedule, current_group_id=data.get('gid'))

    course_themes = CourseTheme.query.all();
    if course_themes:
        all_groups = list()
        for course_theme in course_themes:
            groups = list()
            if course_theme.course_number:
                course_numbers = course_theme.course_number
                for course_number in course_numbers:
                    if course_number.course_group:
                        for group_data in course_number.course_group:
                            groups.append({
                                'id': group_data.id,
                                'gid': group_data.gid
                            })
            all_groups.append({
                 'course_theme_name': course_theme.name,
                 'groups': groups
            })

    return render_template('class_schedule.html', all_groups=all_groups)


@bp_web.route('/class_schedule/edit', methods=['POST'])
@login_required
def class_schedule_edit():
    data = request.form.to_dict()
    if data:
        if data.get('course_group_id'):
            course_group_id = data.pop('course_group_id')
            course_group = CourseGroup.query.get(course_group_id)
            if course_group:
                parsed_data = dict()
                for key,value in data.items():
                    if value:
                        keys = key.split('_')

                        if not keys[0]+keys[1] in parsed_data.keys():
                             parsed_data[keys[0]+keys[1]] = dict()

                        parsed_data[keys[0] + keys[1]]['dow'] = keys[0]
                        parsed_data[keys[0] + keys[1]]['seq'] = keys[1]
                        parsed_data[keys[0] + keys[1]][keys[2]] = value

                class_schedules = course_group.class_schedule.all()
                if class_schedules:
                    for class_schedule in class_schedules:
                        session.delete(class_schedule)

                for row in parsed_data.values():
                    if row['subj']:
                        subj = Subject.query.get(row['subj'])
                        if subj:
                            class_lesson = ClassSchedule()
                            class_lesson.subject = subj
                            class_lesson.course_group = course_group

                            for item in row.items():
                                if item[0] == 'class':
                                    class_lesson.classroom = item[1]
                                if item[0] == 'seq':
                                    class_lesson.seq = int(item[1])
                                if item[0] == 'dow':
                                    class_lesson.dow = item[1]
                            session.add(class_lesson)

                session.commit()

                return redirect(url_for('bp_web.class_schedule'))

