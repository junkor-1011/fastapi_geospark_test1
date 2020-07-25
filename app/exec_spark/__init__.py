"""
***
"""

import pyspark_utils
from .utils import *

# create session (TMP)
spark = pyspark_utils.get_or_create_geospark_session()
