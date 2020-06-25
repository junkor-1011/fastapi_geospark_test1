#!/usr/bin/env sh

# https://qiita.com/koara-local/items/2d67c0964188bba39e29
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

rsync -auv ../../Pipfile ./Pipfile
rsync -auv ../../Pipfile.lock ./Pipfile.lock
rsync -auv ../../app/ ./app/

# rm pycache
# find ./app -name "*pyc" -type f | xargs rm
