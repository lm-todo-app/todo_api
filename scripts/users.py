from getpass import getpass
import click
from flask.cli import AppGroup
from models.user import User
from database import commit_to_db
from authz import Roles

users_cli = AppGroup("users")


@users_cli.command("create")
def create():
    """
    Run: 'flask users create $name'
    Create a normal user, skip email confirmation.
    """
    _create_user(Roles.user)


@users_cli.command("create_superadmin")
def create_superadmin():
    """
    Run: 'flask users create_superadmin'
    Create a superadmin user, skip email confirmation.
    """
    _create_user(Roles.superadmin)


def _create_user(role):
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

    user = User.create(form, autoconfirm=True)
    user.set_role(role)

    if commit_to_db():
        print(f"\nUser {user.username} created successfully!\n")
    else:
        print("\nFailed to create user!\n")
