# -*- coding: utf-8 -*-
"""
read config of SparkDriver

ToDo:
    - except for Import Error is dirty.
      Should be improved.
"""

try:
    from .spark_session import *
except ImportError:
    # ToDo: Improve
    config_tmp = "spark_session_local.py"  # EDIT
    print(f"WARNING: There is NO config: spark_session.py for SparkDriver."
          f"Let's try to use {config_tmp} instead.")
    from . import spark_session_local as spark_session
    from .spark_session_local import *
except Exception as e:
    # TMP
    raise e
