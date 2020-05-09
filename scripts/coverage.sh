#!/bin/bash

pytest --cov .
rm /tmp/todo_test.db
