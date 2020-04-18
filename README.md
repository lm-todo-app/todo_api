# todo_api

---

### Setup

Prerequisites:

- pyenv
- pipenv
- direnv (optional)

Clone repo and then run the following:

`pyenv install 3.8.1`

`pipenv --python 3.8.1 install`

If you have direnv installed run:

`echo "layout pipenv" >> .envrc && direnv allow .`

Remember to add .envrc and .direnv to your global gitignore if using direnv

else run:

`pipenv shell`
`export FLASK_ENV=development`
`flask run`

Setting FLASK_ENV to development as env variable is advised

---

### Flask Migrate

After creating or editing a model:

- run `flask db migrate -m "NAME OF MIGRATION"`
- run `flask db upgrade`

Flask migrations need to be reviewed as they are not always correct.

---

### Tests

To run tests:

`./test.sh`

This can be run on change/save using [entr](http://eradman.com/entrproject/) with:

`ls | entr ./test.sh`

---
