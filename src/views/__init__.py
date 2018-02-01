"""Initialization API."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from webargs.flaskparser import parser

from src.schemas.web import login_post
from src.lib.access import login_manager, validate_uuid
from src.db.models import User
from src.lib.utils import get_config


bp_web = Blueprint('bp_web', __name__)

@bp_web.errorhandler(422)
def handle_unprocessable_entity(err):
    return render_template('login.html', err_msg='Необходимо указать логин и пароль')

@bp_web.errorhandler(401)
def handle_unauthorized_user(err):
    return redirect(url_for('bp_web.login'))

@bp_web.route('/')
# @login_required
def index():
    return render_template('index.html')


# @bp_web.route('/<stream_id>')
# @login_required
# def stream_statistic(stream_id):
#     if validate_uuid(stream_id):
#         stream = Stream.query.get(stream_id)
#         if stream:
#             streams = Stream.query.all()
#             stream_list = [{
#                 'name': entry.name,
#                 'id': entry.id
#             } for entry in streams]
#             return render_template('index.html', stream_name=stream.name, stream_id=stream.id, stream_list=stream_list)
#     return render_template('404.html')


@bp_web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = parser.parse(login_post, request)
        user = User.query.filter_by(email=data.get('email')).first()
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
