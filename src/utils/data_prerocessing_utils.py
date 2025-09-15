import pandas as pd
from src.utils.logger import get_logger
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
# Download required data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

logger = get_logger(name='data_preprocessing_utils')

@staticmethod
def convert_recrods_to_dataframe(records: list[str], columns_name_list: list[str]) -> pd.DataFrame:
    # ["id", "start_time", "end_time", "text"]
    return pd.DataFrame(records, columns=columns_name_list)

@staticmethod
def drop_invalid_text_rows(df: pd.DataFrame, text_column) -> pd.DataFrame:
    """
    Drop rows where the text column has null, empty, or whitespace-only values.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        text_column (str): Name of the text column to check (default: 'text')
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    # Remove rows with null, empty, or whitespace-only text
    cleaned_df = df[
        df[text_column].notna() & 
        (df[text_column].str.strip() != '')
    ].reset_index(drop=True)
    
    return cleaned_df

@staticmethod
def group_rows_with_splitters(df: pd.DataFrame, group_size: int, overlap: int) -> pd.DataFrame:
    grouped_data = []
    
    for i in range(0, len(df), group_size):
        group = df.iloc[i:i+group_size]
        
        if len(group) == 0:
            continue
        
        # Get current group's text
        current_text = ' '.join(group['text'].tolist())
        
        # Get last 10 words from previous group (if exists)
        if i > 0:  # Not the first group
            prev_group_text = grouped_data[-1]['text']  # Previous group's text
            prev_words = prev_group_text.split()
            last_words = ' '.join(prev_words[-overlap:]) if len(prev_words) >= overlap else prev_group_text
            
            # Combine: last 10 words from previous + current text
            combined_text = last_words + ' ' + current_text
        else:
            # First group - no previous text to add
            combined_text = current_text
            
        grouped_row = {
            'id': group['id'].tolist(),                # [1,2,3,4,5]
            'start_time': group['start_time'].iloc[0], # First start_time
            'end_time': group['end_time'].iloc[-1],    # Last end_time  
            'text': combined_text                      # Combined text with overlap
        }
        
        grouped_data.append(grouped_row)
    
    return pd.DataFrame(grouped_data)

@staticmethod
def perform_nlkt(df: pd.DataFrame) -> pd.DataFrame:
    df_processed = df.copy()
    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        if pd.isna(text):
            return ""
        
        try:
            # Lowercase & tokenize
            tokens = word_tokenize(str(text).lower())
            
            clean_tokens = []
            for word in tokens:
                # Remove punctuation & non-alphabetic with regex
                word = re.sub(r'[^a-z]', '', word)
                
                if word and word not in stop_words:
                    clean_tokens.append(word)
                    
            return ' '.join(clean_tokens)
        except LookupError:
            return str(text).lower()

    # Add processed columns
    df_processed['clean_text'] = df_processed['text'].apply(clean_text)
    df_processed['word_count'] = df_processed['text'].apply(
        lambda x: len(str(x).split()) if pd.notna(x) else 0
    )
    return df_processed