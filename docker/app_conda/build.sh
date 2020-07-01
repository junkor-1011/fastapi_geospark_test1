#!/usr/bin/env sh

# https://qiita.com/koara-local/items/2d67c0964188bba39e29
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

if [ -f $SCRIPT_DIR/.env ]; then
    . $SCRIPT_DIR/.env
    cat $SCRIPT_DIR/.env
fi

sh ./fetch.sh

# ref: https://blog.kkty.jp/entry/2019/06/16/214951
tar -czh . | docker build \
        -t ${IMAGE_TAG:-app_fastapi_pyspark_conda} \
        --build-arg BASE_IMAGE=${BASE_IMAGE:-adoptopenjdk:8-jre-hotspot-bionic} \
        --build-arg USER_UID=${USER_UID:-1000} \
        --build-arg PASSWD=${PASSWD:-password} \
        -
