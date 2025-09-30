#!/bin/bash

# fail on any error
set -e

# set environment variables
. ./local/.env

# show environment variables
printenv

# start the application
# TODO we either need to run main.py in a loop or we need to have this script
# run from supervisord so that the script automatically restarts if python dies
python3 main.py
