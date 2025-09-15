import pandas as pd
from src.utils.common_utils import load_params_yaml, save_data
from src.utils.embedding_db_utils import initalize_chroma_db, get_collection, sentence_transformer_model, insert_dataframe

def generate_and_save_embeddings(config: dict, df: pd.DataFrame) -> None:
    db_path = config['model_embedding']['chroma_db_path']
    transformer_model = config['model_embedding']['transformer_model']
    collection_name = config['model_embedding']['db_collection_name']

    db_client = initalize_chroma_db(db_path)
    collection = get_collection(db_client, collection_name)

    model = sentence_transformer_model(transformer_model)
    insert_dataframe(collection, model, df)

    #query = "What April Lyn is talking about?"
    #results = collection.query(
    #    query_texts=[query],
    #    n_results=4
    #)
    #print(results)

def merge_both_data_frames(params_introduction, params_storytelling):
    df_one = pd.read_csv(params_introduction['model_embedding']['input_path'])
    df_one['title'] = 'Improving Video Intorduction'

    df_two = pd.read_csv(params_storytelling['model_embedding']['input_path'])
    df_two['title'] = 'Improving Story Telling'

    merged_df = pd.concat([df_one, df_two], ignore_index=True)
    save_data(merged_df, params_introduction['common']['final_output_path'])
    return merged_df

if __name__ == '__main__':
    params_introduction = load_params_yaml(params_path='configs/introduction.yaml')
    params_storytelling = load_params_yaml(params_path='configs/storytelling.yaml')
    df = merge_both_data_frames(params_introduction, params_introduction)
    generate_and_save_embeddings(params_introduction, df)
    
