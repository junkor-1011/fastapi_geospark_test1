#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
# import sys
import csv
# import pathlib
# import argparse
import logging
# import gc

import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

# conf
from .config import spark_session as conf_spark_session


class SparkDriver:
    """
    Comment:
    """
    conf = None
    # spark = None
    _spark = None

    @property
    def spark(self):
        return self._spark

    @spark.setter
    def spark(self, spark):
        assert isinstance(spark, pyspark.sql.session.SparkSession)
        self._spark = spark

    def __init__(self, ):
        """
        """
        self.createSession()

    def make_conf(self, ):
        """
        """
        # TMP
        return conf_spark_session.conf_list

    def createSession(self, ):
        """
        """
        if self.spark is None:
            appName = conf_spark_session.appName
            master = conf_spark_session.master
            conf_list = self.make_conf()
            spark = SparkSession\
                .builder\
                .appName(appName)\
                .master(master)\
                .enableHiveSupport()\
                .config(conf=SparkConf().setAll(conf_list))\
                .getOrCreate()
            self.spark = spark
        else:
            logging.warning("WARNING: SparkSession is already created.")

    def csv_to_spark(self, input, output, schema_csv):
        """
        """
        if self.spark is None:
            logging.warning("WARNING: NO SparkSession.")
            return False

        spark = self.spark

        # types list
        types = {
            'binary': BinaryType(),
            'string': StringType(),
            'boolean': BooleanType(),
            'tinyint': ByteType(),
            'int': IntegerType(),
            'bigint': LongType(),
            'smallint': ShortType(),
            'float': FloatType(),
            'double': DoubleType(),
            'date': DateType(),
            'timestamp': TimestampType(),
        }

        with open(schema_csv) as f:
            reader = csv.reader(f)

            schema = StructType(
                [StructField(col_name, types[col_type]) for col_name, col_type in reader]
            )

        # read csv
        df = spark.read.csv(input, schema=schema)

        # write snappy.parquet
        df.write.mode("overwrite").parquet(output)
