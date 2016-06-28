#!/usr/bin/env python

from flask.ext.assets import ManageAssets
from flask.ext.script import Manager

from app import app, assets, db
from app.models import User


manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))


@manager.command
def db_create():
    db.create_all()


@manager.command
def db_drop():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
