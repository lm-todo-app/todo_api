import click
from flask.cli import AppGroup


users_cli = AppGroup('users')

@users_cli.command('create')
@click.argument('name')
def create_user(name):
    """
    Run: 'flask users create $name'
    Create a user, skip email confirmation.
    """
    print('hello {}'.format(name))
