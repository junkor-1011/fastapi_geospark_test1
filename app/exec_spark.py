"""exec spark"""

from typing import (
    Optional,
)

import pandas as pd
import pyspark
import pyspark.sql

from .libs.SparkDriver import SparkDriver

# create session (TMP)
sd = SparkDriver()
spark = sd.spark


def get_databases(orient: str="dict") -> dict:
    """get databases"""
    return spark.sql("show databases") \
        .toPandas() \
        .to_dict(orient=orient)


def create_database(db: str) -> dict:
    """
    create database

    ToDo:

        - try, exceptをもう少しうまく使う（status codeを変えるとか）

    """
    try:
        spark.sql(f"create database {db}")
        message = f"success to create db: {db}"
    except Exception as e:
        message = str(e)
    return {"message": message}


def delete_database(
    db: str,
    ifexists: Optional[bool],
    mode: Optional[str],
):
    if ifexists:
        ifexists_option = "IF EXISTS"
    else:
        ifexists_option = ""

    sql = f"""
        DROP DATABASE {ifexists_option} {db} {mode}
    """
    try:
        spark.sql(sql)
        message = f"success to delete db: {db}"
    except Exception as e:
        message = str(e)

    return {"message": message}


def get_tables(orient: str="dict",
               db: str=None) -> dict:
    """get tables"""
    if db is None:
        result = spark.sql("show tables") \
            .toPandas() \
            .to_dict(orient=orient)
    else:
        result = spark.sql(f"show tables from {db}") \
            .toPandas() \
            .to_dict(orient=orient)
    return result
