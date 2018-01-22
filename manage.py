#!/usr/bin/python3
"""Tool for manage project."""
from shutil import rmtree
from pathlib import Path
import datetime
import os
import telebot

from src import create_app
from src.db import db, rq
from src.tests import run_unit_tests
from flask_script import Manager, Command, Shell
from flask_rq2.script import RQManager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app, with_default_commands=False, usage='Manage montecristo instance')

def run():
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT'],
        threaded=True
    )

def cock():
    bot = telebot.TeleBot('516834738:AAFiBE5c-0TDGBQUBY2OvDvHDgh0UNBZrOU')

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        # print(message.from_user.first_name)
        # bot.reply_to(message, u"Hello, welcome to this bot!")
        # bot.send_message(chat_id=message.from_user.id, text='cock')
        # markup = telebot.types.ReplyKeyboardRemove()
        markup = telebot.types.InlineKeyboardMarkup(row_width=6)
        gobtn1 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
        gobtn2 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
        gobtn3 = telebot.types.InlineKeyboardButton(text='Го', callback_data='say_ok')
        markup.row(gobtn1)
        markup.row(gobtn2, gobtn3)
        bot.send_message(chat_id=message.from_user.id, text='Шо го? Камон коуч бой летс ду зис', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'say_ok')
    def test_callback(call):
        bot.send_message(call.from_user.id, text='найс найс')

    # @bot.message_handler(regexp='Похналэ')
    # def alo(message):
    #     print('got it')

    bot.polling()
    # print(bot.get_updates())


tests_command = Command(run_unit_tests)
tests_command.option_list[0].kwargs['nargs'] = '*'

manager.add_command('db', MigrateCommand)
manager.add_command("run", Command(run))
manager.add_command('rq', RQManager(rq))
manager.add_command("test", tests_command)
manager.add_command("shell", Shell())
manager.add_command("cock", Command(cock))

if __name__ == '__main__':
    manager.run()
