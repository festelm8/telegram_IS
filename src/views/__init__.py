"""Initialization API."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser, use_args

from src.schemas.web import login_post, teacher_create_post
from src.lib.access import login_manager, validate_uuid
from src.db import session, db
from src.db.models import User, Teacher
from src.lib.utils import get_config


bp_web = Blueprint('bp_web', __name__)

from src.views import teachers
from src.views import subjects
from src.views import course_themes
from src.views import class_schedule

@bp_web.errorhandler(422)
def handle_unprocessable_entity(err):
    return redirect(url_for('bp_web.index'))


@parser.error_handler
def handle_error(error):
    print('==x=x=x=x=x=x=x=x=x')
    print(error)


@bp_web.errorhandler(401)
def handle_unauthorized_user(err):
    return redirect(url_for('bp_web.login'))


@bp_web.route('/')
@login_required
def index():
    return render_template('index.html')


@bp_web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = parser.parse(login_post, request)
        user = User.query.filter_by(is_admin=True, email=data.get('email')).first()
        if not user:
            return render_template('login.html', err_msg='Пользователь с таким email не существует')
        if not user.verify_password(data.get('password')):
            return render_template('login.html', err_msg='Неверный email или пароль')
        login_user(user)
        return redirect(url_for('bp_web.index'))

    return render_template('login.html', err_msg=None)


@bp_web.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('bp_web.login'))





