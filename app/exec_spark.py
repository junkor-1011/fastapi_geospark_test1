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
