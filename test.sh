#!/bin/sh

export FLASK_ENV=test
export FLASK_RUN_PORT=5001
flask run &
pid=$!
py.test -v
rm /tmp/todo_test.db
kill -9 $pid
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
