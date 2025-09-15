import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from src.utils.logger import get_logger

logger = get_logger('embedding_db_utils')

@staticmethod
def initalize_chroma_db(path: str):
    return chromadb.PersistentClient(path=path)

@staticmethod
def get_collection(db_client, name: str) -> chromadb.Collection:
    return db_client.get_or_create_collection(name=name)

@staticmethod
def sentence_transformer_model(model: str):
    return SentenceTransformer(model)

@staticmethod
def generate_embedding(model, text: str):
    return model.encode(text, convert_to_numpy=True)

@staticmethod
def insert_row(collection, model, row):
    """Insert a single row into Chroma collection."""
    embedding = generate_embedding(model, row["clean_text"])
    metadata = {
        "id": str(row["id"]),
        "start_time": row["start_time"],
        "end_time": row["end_time"],
        "text": row["text"],
        "title": row["title"]
    }
    collection.add(
        ids=[str(row["id"])],
        embeddings=[embedding],
        documents=[row["clean_text"]],
        metadatas=[metadata],
    )

@staticmethod
def insert_dataframe(collection, model, df: pd.DataFrame):
    """Insert entire DataFrame into Chroma collection."""
    for _, row in df.iterrows():
        insert_row(collection, model, row)
    #logger.info(f"Inserted {df.shape[0]} records into Chroma DB.")
    