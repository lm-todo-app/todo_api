from getpass import getpass
from datetime import datetime
import click
from flask.cli import AppGroup
from models.user import create_user
from database import commit_to_db


users_cli = AppGroup("users")


@users_cli.command("create")
@click.argument("name")
def create(name):
    """
    Run: 'flask users create $name'
    Create a normal user, skip email confirmation.
    """
    print("hello {}".format(name))


@users_cli.command("create_superadmin")
def create_superadmin():
    """
    Run: 'flask users create_superadmin'
    Create a super admin user, skip email confirmation.
    """
    form = {}

    form["username"] = input("enter username (required):")
    form["email"] = input("enter email (required):")
    form["firstName"] = input("enter first name:")
    form["firstName"] = input("enter last name:")
    form["password"] = getpass("enter password (required):")
    password_confirm = getpass("enter password again:")

    if form["password"] != password_confirm:
        print("\nPassword does not match!\n")
        return

    form["confirmed_on"] = datetime.now()

    user = create_user(form)
    if commit_to_db():
        print(f"\nUser {user.username} created successfully!\n")
    else:
        print("\nFailed to create user!\n")
