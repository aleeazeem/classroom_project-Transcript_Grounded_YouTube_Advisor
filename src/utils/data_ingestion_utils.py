import pandas as pd
import re
from src.utils.logger import get_logger
from typing import Optional
import yaml


logger = get_logger(name='data_ingestion_utils')

@staticmethod
def open_file(file_path: str) -> Optional[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
    raise Exception

@staticmethod
def remove_title_from_data(file_text: str, text_to_remove: str) -> list[str]:
    if file_text.startswith(text_to_remove):
        file_text = file_text.split('\n', 1)[1] if '\n' in file_text else ''
    
    # Split transcript blocks by double newlines
    return re.split(r'\n\s*\n', file_text.strip())


@staticmethod
def convert_data_to_list(blocks) -> list:
    """
    Convert WEBVTT transcript file to pandas DataFrame.
    
    Args:
        file_path (str): Path to the WEBVTT file
        
    Returns:
        pd.DataFrame: DataFrame with columns [id, start_time, end_time, text]
    """
    
    records = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        
        # Skip if not enough lines for a valid block
        if len(lines) < 3:
            continue
            
        # Try to parse the first line as ID
        try:
            idx = int(lines[0])
        except ValueError:
            continue
        
        # Second line should be the timestamp
        time_range = lines[1]
        
        # Check if it matches timestamp pattern
        if '-->' not in time_range:
            continue
            
        # Rest of the lines are the text
        text = " ".join(lines[2:]).strip()
        
        # Extract start and end times
        try:
            start, end = re.split(r'\s*-->\s*', time_range)
            records.append([idx, start.strip(), end.strip(), text])
        except ValueError:
            print(f"Warning: Could not parse timestamp in block {idx}: {time_range}")
            continue
    return records  
    