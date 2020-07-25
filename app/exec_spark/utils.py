"""exec spark"""

from typing import (
    Optional,
)

import pandas as pd
import pyspark
import pyspark.sql

from .session import spark


def get_databases(orient: str="dict") -> dict:
    """get databases"""
    return spark.sql("show databases") \
        .toPandas() \
        .to_dict(orient=orient)


def describe_database(
    db: str,
    orient: str,
    extended: Optional[bool],
):
    """describe database"""
    if extended:
        sql_query = f"""
            DESCRIBE DATABASE EXTENDED {db}
        """
    else:
        sql_query = f"""
            DESCRIBE DATABASE {db}
        """

    try:
        message = spark.sql(sql_query) \
            .toPandas() \
            .to_dict(orient=orient)
    except Exception as e:
        message = str(e)
    return {"message": message}


def create_database(db: str) -> dict:
    """
    create database

    ToDo:

        - try, exceptをもう少しうまく使う（status codeを変えるとか）

    """
    try:
        spark.sql(f"CREATE DATABASE {db}")
        message = f"success to create db: {db}"
    except Exception as e:
        message = str(e)
    return {"message": message}


def drop_database(
    db: str,
    ifexists: Optional[bool],
    mode: Optional[str],
):
    if ifexists:
        ifexists_option = "IF EXISTS"
    else:
        ifexists_option = ""

    sql_query = f"""
        DROP DATABASE {ifexists_option} {db} {mode}
    """
    try:
        spark.sql(sql_query)
        message = f"success to drop db: {db}"
    except Exception as e:
        message = str(e)

    return {"message": message}


def get_tables(
    db: Optional[str] = "default",
    orient: str="dict",
) -> dict:
    """get tables"""

    sql_query = f"""
        SHOW TABLES FROM {db}
    """
    result = spark.sql(sql_query) \
        .toPandas() \
        .to_dict(orient=orient)
    return result


def read_table(
    db: str = "default",
    table: str = " ",
    limit: int = 100,
    orient: str = "list",
):
    df = spark.table(f"{db}.{table}")

    result = df.limit(limit) \
        .toPandas() \
        .to_dict(orient=orient)
    return result


def drop_table(
    db: str = "default",
    table: str = " ",
    ifexists: Optional[bool] = True,
):
    if ifexists:
        ifexists_opt = "IF EXISTS"
    else:
        ifexists_opt = ""

    sql_query = f"DROP TABLE {ifexists_opt} {db}.{table}"

    try:
        spark.sql(sql_query)
        message = f"success to drop table: {db}.{table}"
    except Exception as e:
        message = str(e)

    return {"message": message}


def get_table_info(
    db: str = "default",
    table: str = " ",
    extended: Optional[bool] = None,
    orient: str = "dict",
):
    if extended:
        extended_opt = "EXTENDED"
    else:
        extended_opt = ""

    sql_query = f"DESCRIBE {extended_opt} {db}.{table}"
    result = spark.sql(sql_query) \
        .toPandas() \
        .to_dict(orient=orient)
    return result
