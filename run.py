import os
# import pytest
import click
# from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import g, session
from app import create_app
from utils.database import db
# from dotenv import load_dotenv
# from seeders import seed_db, SEED_OPTIONS
# from flask_user import UserManager
from users.models import User


# load_dotenv()


app = create_app(os.getenv('FLASK_ENV', 'development'))
# migrate = Migrate(app, db)
# manager = Manager(app)


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        username = session['username']
        get_user = lambda username: User.query.filter_by(username=username).first() 
        g.user = get_user(username) if username else None
    # print(f'\n\n G user at start of request {g.user} {session.items()}')

@app.after_request
def after_request(response):
    db.session.remove()
    return response


def _make_context():
    return dict(app=app, db=db)

# @app.cli.command(context_settings=dict(token_normalize_func=str.lower))
# @click.argument('entity_name', required=False)
# @click.option(
#     '--entity_name',
#     help='The Resource/Entity name you want to seed.',
#     type=click.Choice(SEED_OPTIONS))
# @manager.command
# def seed(entity_name):
#     """
#     Seeds the database with sample data

#     Args:
#         resource_name (string): The resource name you want to seed
#     Return:
#         func: call the function if successful or the click help option if unsuccesful
#     """
#     seed_db(entity_name=entity_name)


# @manager.command
# def test():
#     pytest.main(["-s", "tests/"])


# @manager.command
# def test_coverage():
#     pytest.main(["--cov=.", "tests/"])


# @manager.command
# def test_cov_report():
#     pytest.main(["--cov-report", "html:cov_html",
#                  "--cov=.", "tests/"])


# Turn on reloader
# manager.add_command('runserver', Server(
#     use_reloader=True,
#     host=os.getenv('IP', '0.0.0.0'),
#     port=int(os.getenv('PORT', 5000))
# ))

# # Migrations
# manager.add_command('db', MigrateCommand)


# manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == '__main__':
    # manager.run()
    app.run()
