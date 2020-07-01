ARG BASE_IMAGE=adoptopenjdk:8-jre-hotspot-bionic
FROM ${BASE_IMAGE}

# system update & package install
RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends \
    unzip bzip2 \
    openssl libssl-dev \
    curl wget \
    ca-certificates \
    fontconfig \
    locales \
    bash \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    # build-essential \
# todo: 要不要の選別など



# SPARK
# https://qiita.com/hrkt/items/fe9b1162f7a08a07e812
ARG SPARK_VERSION=3.0.0
ARG HADOOP_VERSION=3.2
RUN curl -O http://apache.mirror.iphh.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz


# user
# ref:
# https://zukucode.com/2019/06/docker-user.html
# https://qiita.com/Riliumph/items/3b09e0804d7a04dff85b
# 一般ユーザーアカウントを追加
ENV USER_NAME=app
ARG USER_UID=1000
ARG PASSWD=password

RUN useradd -m -s /bin/bash -u ${USER_UID} ${USER_NAME} && \
    gpasswd -a ${USER_NAME} sudo && \
    echo "${USER_NAME}:${PASSWD}" | chpasswd && \
    echo "${USER_NAME} ALL=(ALL) ALL" >> /etc/sudoers && \
    chmod g+w /etc/passwd
# 一般ユーザーにsudo権限を付与
#RUN gpasswd -a ${UID} sudo

# conda
ENV CONDA_DIR=/opt/conda \
    HOME=/home/$USER_NAME \
    SHELL=/bin/bash
RUN mkdir -p $CONDA_DIR && \
    chown $USER_NAME:$USER_UID $CONDA_DIR
# conda package-info
COPY ./conda_packages.yml /tmp/conda_packages.yml


# ubuntu color-prompt
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc


USER ${USER_UID}

WORKDIR $HOME
ARG PYTHON_VERSION=default
# miniconda
# ARG MINICONDA_VERSION=py38_4.8.3-Linux-x86_64
ARG MINICONDA_VERSION=py37_4.8.3-Linux-x86_64
# ARG MINICONDA_MD5=d63adf39f2c220950a063e0529d4ff74
ARG MINICONDA_MD5=751786b92c00b1aeae3f017b781018df
ENV PATH=${CONDA_DIR}/bin:$PATH

RUN cd /tmp && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh && \
    echo "${MINICONDA_MD5} *Miniconda3-${MINICONDA_VERSION}.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}.sh && \
    echo "conda ${CONDA_VERSION}" >> $CONDA_DIR/conda-meta/pinned && \
    conda config --system --prepend channels conda-forge && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda config --system --set channel_priority strict && \
    if [ ! $PYTHON_VERSION = 'default' ]; then conda install --yes python=$PYTHON_VERSION; fi && \
    conda list python | grep '^python ' | tr -s ' ' | cut -d '.' -f 1,2 | sed 's/$/.*/' >> $CONDA_DIR/conda-meta/pinned && \
    conda install --quiet --yes conda && \
    conda install --quiet --yes pip && \
    conda update --all --quiet --yes

# Install Tini
# RUN conda install --quiet --yes 'tini=0.18.0' && \
#     conda list tini | grep tini | tr -s ' ' | cut -d ' ' -f 1,2 >> $CONDA_DIR/conda-meta/pinned && \
#     conda clean --all -f -y

# install packages
RUN conda env update -n base -f /tmp/conda_packages.yml && \
    conda clean --all -f -y && \
    rm -rf $HOME/.cache/yarn



# app

USER root

# https://medium.com/@rlagowski/create-flask-app-with-uwsgi-nginx-certbot-for-ssl-and-all-this-with-docker-a9f23516618d
# 運用時はコンテナイメージ内にソースコードを含める
COPY ./app /app/app
COPY ./scripts /app/scripts
RUN mkdir /app/db && \
    mkdir /app/hive-db
# COPY ./init_project /app/init_project
RUN chown -R ${USER_NAME}:${USER_NAME} /app
# --chown= では環境変数の代入が効かない


USER ${USER_UID}
WORKDIR /app


# Configration

# java
ENV JAVA_HOME=/opt/java/openjdk \
    PATH="/opt/java/openjdk/bin:$PATH"

# pyspark
ARG PY4J_VER=0.10.9
ENV SPARK_HOME=/usr/local/spark
ENV PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-${PY4J_VER}-src.zip \
    SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH=$PATH:${SPARK_HOME}/bin \
    PYSPARK_PYTHON=${CONDA_DIR}/bin/python \
    PYSPARK_DRIVER=${CONDA_DIR}/bin/python



EXPOSE 8000

ENV PROJECT_HOME=/app \
    SPARK_WAREHOUSE_HOME=/app/hive-db/spark-warehouse \
    HIVE_METASTORE_DB_HOME=/app/hive-db \
    PYTHONPATH=/app/app/libs:$PYTHONPATH \
    PATH=/app/scripts/project_bin:$PATH

# Execute
CMD ["run_app"]

