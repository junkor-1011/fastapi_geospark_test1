#!/usr/bin/env sh

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

rsync -auv --copy-links ../../app/ ./app/
rsync -auv --copy-links ../../scripts/ ./scripts/
# rsync -auv ../../init_project ./init_project

# TMP
if [ -f $SCRIPT_DIR/scripts/custom_setting ]; then
    rm $SCRIPT_DIR/scripts/custom_setting
fi

# rm pycache
# find ./app -name "*pyc" -type f | xargs rm
