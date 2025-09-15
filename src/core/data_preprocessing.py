import pandas as pd
from src.utils.common_utils import save_data
from src.utils.data_prerocessing_utils import drop_invalid_text_rows, group_rows_with_splitters, perform_nlkt
from src.utils.common_utils import save_data, load_params_yaml
from src.utils.logger import get_logger

logger = get_logger('data_preprocessing')

def main(config: dict) -> None:
    try:
        input_file_path: str = config['data_preprocessing']['input_path'] # that will be route to folder transcripts where data exists
        output_file_path: str = config['data_preprocessing']['output_path']
        group_size: int = config['data_preprocessing']['group_size']
        overlap: int = config['data_preprocessing']['overlap']

        df = pd.read_csv(input_file_path)
        df = drop_invalid_text_rows(df, 'text')
        df = group_rows_with_splitters(df, group_size, overlap)
        df = perform_nlkt(df)
        save_data(df, output_file_path)
    except Exception as e:
        logger.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    params_introduction = load_params_yaml(params_path='configs/introduction.yaml')
    main(params_introduction)

    params_storytelling = load_params_yaml(params_path='configs/storytelling.yaml')
    main(params_storytelling)

