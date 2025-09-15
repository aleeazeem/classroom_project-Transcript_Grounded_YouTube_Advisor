import pandas as pd
import yaml
from src.utils.data_ingestion_utils import open_file, remove_title_from_data, convert_data_to_list
from src.utils.data_prerocessing_utils import convert_recrods_to_dataframe
from src.utils.common_utils import save_data, load_params_yaml
from src.utils.logger import get_logger

logger = get_logger('data_ingestion')

def main(config: dict, columns_list: list[str]) -> None:
    """
    Get data file text file and convert into data frame.
    The file will be saved in the form of csv file under output_files folder
    Args:
        config: Coming from trans_params.yaml file. input_path where actual file exists & output_path where file will be saved after process
        columns_list: list to name each column in the data frame
        
    Returns:
        pd.DataFrame: DataFrame with columns [id, start_time, end_time, text]
    """

    try:
        input_file_path: str = config['data_ingestion']['input_path'] # that will be route to folder transcripts where data exists
        output_file_path: str = config['data_ingestion']['output_path']
        file_text = open_file(input_file_path)
        blocks = remove_title_from_data(file_text, 'WEBVTT')
        data_list = convert_data_to_list(blocks)
        df = convert_recrods_to_dataframe(data_list, columns_list)
        save_data(df, output_file_path)
    except Exception as e:
        logger.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")
    

if __name__ == '__main__':
    params_introduction = load_params_yaml(params_path='configs/introduction.yaml')
    params_storytelling = load_params_yaml(params_path='configs/storytelling.yaml')
    columns_list = ["id", "start_time", "end_time", "text"]
    main(params_introduction, columns_list)
    main(params_storytelling, columns_list)