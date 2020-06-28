"""exec spark"""

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
