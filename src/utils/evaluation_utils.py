import json
from typing import List, Dict

class TranscriptEvaluator:
    def __init__(self, collection):
        """
        collection: ChromaDB collection (already loaded with embeddings + metadata).
        """
        self.collection = collection

    def query(self, question: str, k: int = 5) -> List[Dict]:
        """Query collection and return retrieved chunks with metadata."""
        results = self.collection.query(query_texts=[question], n_results=k)

        retrieved_chunks = [
            {
                "title": meta["title"],       # only keep title for evaluation
                "id": meta.get("id"),
                "start_time": meta.get("start_time"),
                "end_time": meta.get("end_time"),
                "clean_text": doc
            }
            for meta, doc in zip(results["metadatas"][0], results["documents"][0])
        ]
        return retrieved_chunks

    @staticmethod
    def precision_at_k(retrieved, relevant, k):
        retrieved_titles = {r["title"] for r in retrieved[:k]}
        relevant_titles = {r["title"] for r in relevant}
        return len(retrieved_titles & relevant_titles) / k

    @staticmethod
    def recall_at_k(retrieved, relevant, k):
        retrieved_titles = {r["title"] for r in retrieved[:k]}
        relevant_titles = {r["title"] for r in relevant}
        return len(retrieved_titles & relevant_titles) / len(relevant_titles)

    @staticmethod
    def accuracy_at_k(retrieved, relevant, k):
        retrieved_titles = {r["title"] for r in retrieved[:k]}
        relevant_titles = {r["title"] for r in relevant}
        return int(len(retrieved_titles & relevant_titles) > 0)

    def evaluate(self, ground_truth: Dict[str, List[Dict]], k: int = 5):
        """
        ground_truth: dict mapping { query: [list of relevant chunks] }
        Each relevant chunk must contain at least "title".
        """
        results = {}
        for query, relevant_chunks in ground_truth.items():
            retrieved_chunks = self.query(query, k)

            p = self.precision_at_k(retrieved_chunks, relevant_chunks, k)
            r = self.recall_at_k(retrieved_chunks, relevant_chunks, k)
            a = self.accuracy_at_k(retrieved_chunks, relevant_chunks, k)

            results[query] = {"precision": p, "recall": r, "accuracy": a}
        return results
