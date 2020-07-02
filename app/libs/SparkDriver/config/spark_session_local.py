# -*- coding: utf-8 -*-
"""
spark_session.py template(local)

ToDo:
    - より扱いやすい形式(公式なSparkのconfigファイルなど)で書いたファイルを
      読み込んでパースするようにする
    - 共通部分は ``__init__.py`` などの中で行うようにするなど、共通部分の抜き出し
"""

from pathlib import Path
import os
# import sys

# set default
PROJECT_HOME_DEFAULT = Path(os.path.dirname(__file__)).parent.parent.parent
SPARK_WAREHOUSE_HOME_DEFAULT = str(
    PROJECT_HOME_DEFAULT / "hive-db" / "spark-warehouse"
)
HIVE_METASTORE_DB_HOME_DEFAULT = str(
    PROJECT_HOME_DEFAULT / "hive-db"
)

# read env & set constants
PROJECT_HOME = os.getenv(
    "PROJECT_HOME", PROJECT_HOME_DEFAULT
)
SPARK_WAREHOUSE_HOME = os.getenv(
    "SPARK_WAREHOUSE_HOME", SPARK_WAREHOUSE_HOME_DEFAULT
)
HIVE_METASTORE_DB_HOME = os.getenv(
    "HIVE_METASTORE_DB_HOME", HIVE_METASTORE_DB_HOME_DEFAULT
)

appName = "local-test"
master = "local[*]"
conf_list = [
    ["spark.sql.execution.arrow.pyspark.enabled", "true"],
    ["spark.serializer", "org.apache.spark.serializer.KryoSerializer"],
    ["spark.kryoserializer.buffer.max", "1024m"],
    ["spark.driver.maxResultSize", "6g"],
    ["spark.memory.offHeap.enabled", "true"],
    ["spark.memory.offHeap.size", "4096"],
    ["spark.driver.memory", "2g"],
    ["spark.executor.memory", "6g"],
    ["spark.sql.session.timeZone", "Etc/UTC"],
    # ["spark.eventLog.enabled", "true"],
    ["spark.sql.warehouse.dir", SPARK_WAREHOUSE_HOME],
    ["spark.executor.extraJavaOptions", "-Duser.timezone=Etc/UTC"],
    ["spark.driver.extraJavaOptions",
     f"-Duser.timezone=Etc/UTC -Dderby.system.home='{HIVE_METASTORE_DB_HOME}'"],
]
