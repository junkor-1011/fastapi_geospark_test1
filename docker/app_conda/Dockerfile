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

# TINI
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

# SPARK
# https://qiita.com/hrkt/items/fe9b1162f7a08a07e812
ARG SPARK_VERSION=2.4.6
ARG HADOOP_VERSION=2.7
ENV SPARK_HOME=/usr/local/spark
RUN curl -O http://apache.mirror.iphh.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
# add jar
RUN echo "spark.jars.packages org.postgresql:postgresql:42.2.14,org.datasyslab:geospark:1.3.1,org.datasyslab:geospark-sql_2.3:1.3.1,org.datasyslab:geospark-viz_2.3:1.3.1" >> $SPARK_HOME/conf/spark-defaults.conf && \
    chmod +r $SPARK_HOME/conf/spark-defaults.conf

# user
ENV USER_NAME=app
ARG USER_UID=1000
ARG PASSWD=password

RUN useradd -m -s /bin/bash -u ${USER_UID} ${USER_NAME} && \
    gpasswd -a ${USER_NAME} sudo && \
    echo "${USER_NAME}:${PASSWD}" | chpasswd && \
    echo "${USER_NAME} ALL=(ALL) ALL" >> /etc/sudoers && \
    chmod g+w /etc/passwd

# conda
ENV CONDA_DIR=/opt/conda \
    CONDA_TMP_DIR=/tmp/conda \
    HOME=/home/$USER_NAME \
    SHELL=/bin/bash
RUN mkdir -p $CONDA_DIR && \
    mkdir -p $CONDA_TMP_DIR && \
    chown $USER_NAME:$USER_UID $CONDA_DIR && \
    chown $USER_NAME:$USER_UID $CONDA_TMP_DIR
# conda package-info
ARG CONDA_YAML="./conda_packages.yml"
COPY $CONDA_YAML /tmp/conda_packages.yml
# prevent pip-error (tmp)
# RUN sed -i -e 's/python-graphviz/graphviz/' /tmp/conda_packages.yml


# ubuntu color-prompt
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc


USER ${USER_UID}

WORKDIR $HOME
ARG PYTHON_VERSION=default
# miniconda
ARG MINICONDA_VERSION=py38_4.8.3-Linux-x86_64
ARG MINICONDA_MD5=d63adf39f2c220950a063e0529d4ff74
ENV PATH=${CONDA_DIR}/bin:$PATH

RUN cd /tmp && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}.sh && \
    echo "${MINICONDA_MD5} *Miniconda3-${MINICONDA_VERSION}.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}.sh -f -b -p $CONDA_TMP_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}.sh && \
    $CONDA_TMP_DIR/bin/conda env create -f /tmp/conda_packages.yml --prefix $CONDA_DIR && \
    rm -rf $HOME/.cache/* && \
    rm -rf $CONDA_TMP_DIR/*


# app

USER root

# https://medium.com/@rlagowski/create-flask-app-with-uwsgi-nginx-certbot-for-ssl-and-all-this-with-docker-a9f23516618d
# 運用時はコンテナイメージ内にソースコードを含める
COPY ./app /app/app
COPY ./scripts /app/scripts
RUN mkdir -p /app/data/db && \
    mkdir -p /app/data/hive-db
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
ARG PY4J_VER=0.10.7
ENV SPARK_HOME=/usr/local/spark
ENV PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-${PY4J_VER}-src.zip \
    SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH=$PATH:${SPARK_HOME}/bin \
    PYSPARK_PYTHON=${CONDA_DIR}/bin/python \
    PYSPARK_DRIVER=${CONDA_DIR}/bin/python \
    ARROW_PRE_0_15_IPC_FORMAT=1

RUN $SPARK_HOME/bin/spark-shell --packages org.postgresql:postgresql:42.2.14,org.datasyslab:geospark:1.3.1,org.datasyslab:geospark-sql_2.3:1.3.1,org.datasyslab:geospark-viz_2.3:1.3.1

RUN pip install geospark && \
    rm -rf $HOME/.cache/pip/*


EXPOSE 8000

ENV PROJECT_HOME=/app \
    SPARK_WAREHOUSE_HOME=/app/data/hive-db/spark-warehouse \
    HIVE_METASTORE_DB_HOME=/app/data/hive-db \
    PYTHONPATH=/app/app/libs/pyspark_utils:$PYTHONPATH \
    PATH=/app/scripts/project_bin:$PATH

# Execute
CMD ["run_app"]
