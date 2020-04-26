#!/bin/bash

find . -type f -name "*.py" | xargs pylint

# pylint --load-plugins pylint_flask *.py
