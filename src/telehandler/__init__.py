"""Initialization API."""
from flask import Blueprint, request, g, current_app
import time
import telebot
import json

from src.db.models import CourseTheme, CourseNumber, CourseGroup, Subject, ClassSchedule, User
from src.db import session

bp_tele = Blueprint('bp_tele', __name__)
secret = '516834738:AAFiBE5c-0TDGBQUBY2OvDvHDgh0UNBZrOU'
tbot = telebot.TeleBot(secret)
tbot.remove_webhook()
tbot.set_webhook(url="https://1b684ef4.ngrok.io/{}".format(secret))


@bp_tele.route('/'+secret, methods=['POST'])
def webhook():
    # return "ok", 200
    updates = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))

    if updates.message:
        if updates.message.text == '/start':
            send_welcome(updates.message)
        if updates.message.text == '\U0001F4DA Мои предметы':
            get_my_subjects(updates.message)
        if updates.message.text == '\U0001F558 Расписание':
            get_dows(updates.message)
        if updates.message.text == '\u26F3 Переподписаться':
            send_welcome(updates.message)

    if updates.callback_query:
        data = updates.callback_query.data.split(':')

        if data[0] == 'get_cn':
            get_course_numers(ct_id=data[1], tid=updates.callback_query.from_user.id)
        if data[0] == 'get_cg':
            get_course_groups(cn_id=data[1], tid=updates.callback_query.from_user.id)
        if data[0] == 'subs':
            subscribe(cg_id=data[1], tid=updates.callback_query.from_user.id)
        if data[0] == 'show_subj':
            subject_info(subj_id=data[1], tid=updates.callback_query.from_user.id)
        if data[0] == 'class_schedule':
            class_schedule(dow=data[1], tid=updates.callback_query.from_user.id)

        tbot.answer_callback_query(callback_query_id=updates.callback_query.id)

    return "ok", 200


def send_welcome(message):
    user = User.query.filter_by(tid=message.from_user.id).first()
    if not user:
        user = User(
            tid=message.from_user.id,
            is_admin=False
        )
        session.add(user)
        session.commit()

    course_themes = CourseTheme.query.all()
    markup = telebot.types.InlineKeyboardMarkup(row_width=6)
    for ct in course_themes:
        markup.row(
            telebot.types.InlineKeyboardButton(
                text=ct.name,
                callback_data=':'.join(['get_cn', str(ct.id)])
            )
        )
    tbot.send_message(chat_id=message.from_user.id, text='\U0001F680 Выберите Ваше направление подготовки', reply_markup=markup)


def get_course_numers(ct_id, tid):
    ct = CourseTheme.query.get(ct_id)
    if ct and ct.course_number:
        markup = telebot.types.InlineKeyboardMarkup(row_width=6)
        for cn in ct.course_number:
            markup.row(
                telebot.types.InlineKeyboardButton(
                    text=cn.number,
                    callback_data=':'.join(['get_cg', str(cn.id)])
                )
            )
        tbot.send_message(chat_id=tid, text='\U0001F4DA Выберите Ваш номер курса', reply_markup=markup)


def get_course_groups(cn_id, tid):
    cn = CourseNumber.query.get(cn_id)
    if cn and cn.course_group:
        markup = telebot.types.InlineKeyboardMarkup(row_width=6)
        for cg in cn.course_group:
            markup.row(
                telebot.types.InlineKeyboardButton(
                    text=cg.gid,
                    callback_data=':'.join(['subs', str(cg.id)])
                )
            )
        tbot.send_message(chat_id=tid, text='\U0001F60E Выберите Вашу группу', reply_markup=markup)


def subscribe(cg_id, tid):
    user = User.query.filter_by(tid=tid).first()
    cg = CourseGroup.query.get(cg_id)
    if user and cg and user.course_group and user.course_group.id != cg_id:
        user.course_group = cg
        session.commit()

    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row(telebot.types.KeyboardButton('\U0001F4DA Мои предметы'))
    markup.row(telebot.types.KeyboardButton('\U0001F558 Расписание'))
    markup.row(telebot.types.KeyboardButton('\u26F3 Переподписаться'))

    tbot.send_message(chat_id=tid, text='\u2705 Вы успешно подписались на группу '+str(cg.gid)+'!', reply_markup=markup)


def get_my_subjects(message):
    user = User.query.filter_by(tid=message.from_user.id).first()
    if user:
        subjects = user.course_group.course_number.subjects
        if subjects:
            markup = telebot.types.InlineKeyboardMarkup(row_width=6)
            for subject in subjects:
                markup.row(
                    telebot.types.InlineKeyboardButton(
                        text=subject.name,
                        callback_data=':'.join(['show_subj', str(subject.id)])
                    )
                )
            tbot.send_message(chat_id=message.from_user.id, text='\u2753 Выберите предмет, чтобы получить информацию', reply_markup=markup)


def subject_info(subj_id, tid):
    subj = Subject.query.get(subj_id)
    if subj:
        text = 'Название: {subject}\r\nПреподаватель: {teacher}\r\nEmail преподавателя: {teacher_email}\r\nОписание: {subject_desc}'.format(**dict(
            subject=subj.name,
            teacher=subj.teacher.name,
            teacher_email=subj.teacher.email,
            subject_desc=subj.desc
        ))
        tbot.send_message(chat_id=tid, text=text)


def get_dows(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=6)
    markup.row(
        telebot.types.InlineKeyboardButton(
            text='Пон',
            callback_data=':'.join(['class_schedule', 'mon'])
        ),
        telebot.types.InlineKeyboardButton(
            text='Втор',
            callback_data=':'.join(['class_schedule', 'tue'])
        ),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(
            text='Ср',
            callback_data=':'.join(['class_schedule', 'wed'])
        ),
        telebot.types.InlineKeyboardButton(
            text='Четв',
            callback_data=':'.join(['class_schedule', 'thu'])
        ),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(
            text='Пят',
            callback_data=':'.join(['class_schedule', 'fri'])
        ),
        telebot.types.InlineKeyboardButton(
            text='Суб',
            callback_data=':'.join(['class_schedule', 'sat'])
        ),
    )
    tbot.send_message(chat_id=message.from_user.id, text='\U0001F4C5 Выберите день недели', reply_markup=markup)


def class_schedule(dow, tid):
    user = User.query.filter_by(tid=tid).first()
    if user:
        schedule = user.course_group.class_schedule.filter_by(dow=dow).order_by(ClassSchedule.seq).all()
        if schedule:
            text = str()
            for lection in schedule:
                text += '\U0001F4D6 '+str(lection.seq)+' пара: '+lection.subject.name+' ('+lection.classroom+' ауд.)\r\n'
            tbot.send_message(chat_id=tid, text=text)
        else:
            tbot.send_message(chat_id=tid, text='\U0001F614 Расписание отуствует на указанный день')


def alert_students(group_id, msg):
    if group_id:
        group = CourseGroup.query.get(group_id)
        if group and group.students:
            for student in group.students:
                tbot.send_message(chat_id=student.tid, text=msg)
    else:
        users = User.query.filter_by(is_admin=False).all()
        if users:
            for user in users:
                tbot.send_message(chat_id=user.tid, text=msg)