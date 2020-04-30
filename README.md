[![Build Status](https://travis-ci.com/lm-todo-app/todo_api.svg?branch=master)](https://travis-ci.com/lm-todo-app/todo_api)
[![Coverage Status](https://coveralls.io/repos/github/lm-todo-app/todo_api/badge.svg?branch=master)](https://coveralls.io/github/lm-todo-app/todo_api?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d773b279472a4f6eab6d69d8b602c2ab)](https://www.codacy.com/gh/lm-todo-app/todo_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lm-todo-app/todo_api&amp;utm_campaign=Badge_Grade)

---

## Setup

Prerequisites:

-   pyenv
-   pipenv
-   direnv (optional)

Clone repo and then run the following:

`pyenv install 3.8.1`

`pipenv --python 3.8.1 install --dev`

If you have direnv installed run:

`echo "layout pipenv" >> .envrc && direnv allow .`

Remember to add .envrc and .direnv to your global gitignore if using direnv

else run:

`pipenv shell`
`export FLASK_ENV=development`
`flask run`

Setting FLASK_ENV to development as env variable is advised

---

## Flask Migrate

After creating or editing a model:

-   run `flask db migrate -m "NAME OF MIGRATION"`
-   run `flask db upgrade`

Flask migrations need to be reviewed as they are not always correct.

---

## Tests

To run tests:

`./scripts/test.sh`

This can be run on change/save using [entr](http://eradman.com/entrproject/) with:

`ls | entr ./scripts/test.sh`

---
