#!/usr/bin/python3
"""Tool for manage project."""
from shutil import rmtree
from pathlib import Path
import datetime
import os

from src import create_app
from src.db import db, rq
from src.tests import run_unit_tests
from src.lib.db import include_url_to_config
from src.lib.context import shel_context
from flask_script import Manager, Command, Shell
from flask_rq2.script import RQManager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
migrate = Migrate(app, db)
migrate.configure_callbacks.append(include_url_to_config)

manager = Manager(app, with_default_commands=False, usage='Manage montecristo instance')

def run():
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT'],
        threaded=True
    )


tests_command = Command(run_unit_tests)
tests_command.option_list[0].kwargs['nargs'] = '*'

manager.add_command('db', MigrateCommand)
manager.add_command("run", Command(run))
manager.add_command('rq', RQManager(rq))
manager.add_command("test", tests_command)
manager.add_command("shell", Shell(make_context=shel_context))

if __name__ == '__main__':
    manager.run()
