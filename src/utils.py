import os
import sys
import dill
import pickle

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging


def save_object(file_path, object):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "w") as file_obj:
            pickle.dump(object, file_obj)

    except Exception as e:
        raise CustomException(e, sys)