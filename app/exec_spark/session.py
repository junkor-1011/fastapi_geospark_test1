"""
spark session
"""
from pyspark_utils import get_or_create_geospark_session

spark = get_or_create_geospark_session()

# todo: sparkContext, sqlContext
