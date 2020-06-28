export PROJECT_HOME=$(cd $(dirname $0)/..; pwd)
export SPARK_WAREHOUSE_HOME=$PROJECT_HOME/hive-db/spark-warehouse
export HIVE_METASTORE_DB_HOME=$PROJECT_HOME/hive-db

export PYTHONPATH=$PROJECT_HOME/app/libs:$PYTHONPATH
