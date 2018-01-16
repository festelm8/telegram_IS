#!/usr/bin/python3
"""Tool for manage project."""
from shutil import rmtree
from pathlib import Path
import datetime
import os

from src import create_app
from src.db import db, rq
from src.tests import run_unit_tests
from flask_script import Manager, Command, Shell
from flask_rq2.script import RQManager
from flask_migrate import Migrate, MigrateCommand
from src.lib.bg_checker import streams_list_checker


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

def checker(activate=False, deactivate=False, status=False):
    scheduler = rq.get_scheduler(interval=int(app.config['CHECKING_DELAY'] / 2))
    if status:
        if scheduler.get_jobs():
            print('* enabled')
        else:
            print('* disabled')
        return

    if activate:
        if not scheduler.get_jobs():
            print('*** BG CHECKER activated ***')
            streams_list_checker.schedule(datetime.datetime.utcnow(), interval=app.config['CHECKING_DELAY'])
        else:
            print('* already activated')
        return

    if deactivate:
        print('*** BG CHECKER deactivated ***')
        jobs = scheduler.get_jobs()
        for job in jobs:
            scheduler.cancel(job)
        return

    print('*** BG CHECKER is run ***')
    print('* Start time: '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    scheduler.run()


tests_command = Command(run_unit_tests)
tests_command.option_list[0].kwargs['nargs'] = '*'

manager.add_command('db', MigrateCommand)
manager.add_command("run", Command(run))
manager.add_command("checker", Command(checker))
manager.add_command('rq', RQManager(rq))
manager.add_command("test", tests_command)
manager.add_command("shell", Shell())

if __name__ == '__main__':
    manager.run()
