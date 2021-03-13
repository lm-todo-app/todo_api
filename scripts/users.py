import click
from flask import Blueprint


users_script_bp = Blueprint('users', __name__)

@users_script_bp.cli.command("create")
@click.argument("name")
def create(name):
    """
    Run: 'flask users create $name'
    Create a user, skip email confirmation.
    """
    print('hello {}'.format(name))
