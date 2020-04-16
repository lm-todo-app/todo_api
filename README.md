# todo_api

## Setup

Prerequisites:

- pyenv
- pipenv
- direnv (optional)

Clone repo and then run the following:

`pyenv install 3.8.1`

`pipenv --python 3.8.1 install`

If you have direnv installed run:

`echo "layout pipenv" >> .envrc && direnv allow .`

*Note: remember to add .envrc and .direnv to your global gitignore when using direnv*

else run:

`pipenv shell`

---

Flask Migrate

After creating or editing a model:

- run `flask db migrate -m "NAME OF MIGRATION"`
- run `flask db upgrade`

_Note: Flask migrations need to be reviewed as they are not always correct._
