#!/usr/bin/env sh

# https://qiita.com/koara-local/items/2d67c0964188bba39e29
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

sh ./fetch.sh

# ref: https://blog.kkty.jp/entry/2019/06/16/214951
tar -czh . | docker build \
        -t app_fastapi_py38 \
        --build-arg BASE_IMAGE=python:3.8-slim-buster \
        --build-arg USER_UID=1000 \
        -
