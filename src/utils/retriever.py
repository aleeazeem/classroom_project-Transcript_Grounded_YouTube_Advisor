import chromadb
from dotenv import load_dotenv

load_dotenv()


class Retriever:
    def __init__(self, path: str = "./chroma_db", collection_name: str = "video_transcripts"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_collection(collection_name)

    def query(self, question: str, k: int = 3):
        """Query ChromaDB and return top-k chunks with metadata."""
        results = self.collection.query(query_texts=[question], n_results=k)

        if not results["documents"][0]:
            return []

        chunks = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            chunks.append({
                "title": meta.get("title", "Unknown"),
                "start_time": meta.get("start_time"),
                "end_time": meta.get("end_time"),
                "clean_text": doc
            })
        return chunks
