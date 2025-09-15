from typing import Any
from src.utils.logger import get_logger
import pandas as pd
import os
from datetime import datetime, timedelta
import math
import yaml

logger = get_logger('common_utils')

@staticmethod
def load_params_yaml(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise

@staticmethod
def save_data(df: Any, file_path: str) -> None:
    """Save the dataframe to a CSV file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.debug('Data saved to %s', file_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

@staticmethod
def round_time_string(time_str: str, kind: str = "start") -> str:
    """
    Round a time string (HH:MM:SS.sss) to floor (start) or ceil (end).

    Args:
        time_str (str): Timestamp like '00:47:14.185'
        kind (str): 'start' -> floor, 'end' -> ceil

    Returns:
        str: Rounded time string in HH:MM:SS format
    """
    # Parse time string
    dt = datetime.strptime(time_str, "%H:%M:%S.%f")

    # Total seconds since midnight
    total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6

    if kind == "start":
        rounded_seconds = math.floor(total_seconds)
    elif kind == "end":
        rounded_seconds = math.ceil(total_seconds)
    else:
        raise ValueError("kind must be 'start' or 'end'")

    # Convert back to HH:MM:SS
    rounded_time = str(timedelta(seconds=rounded_seconds))

    # Force HH:MM:SS format with zero padding
    return str(datetime.strptime(rounded_time, "%H:%M:%S").time())
