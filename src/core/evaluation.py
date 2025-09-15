from src.utils.evaluation_utils import TranscriptEvaluator
import chromadb
import os
import json


def main():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("video_transcripts")

    ground_truth = {
        "how can you improve happiness in video introduction": [
            {
                "title": "Improving Video Intorduction"
            }
        ],
        "what visuals should be used in storytelling": [
            {
                "title": "Improving Story Telling"
            }
        ]
    }

    # Run evaluation
    evaluator = TranscriptEvaluator(collection)
    results = evaluator.evaluate(ground_truth, k=3)

    for query, metrics in results.items():
        print(f"\nQuery: {query}")
        print(f"Precision@3: {metrics['precision']:.2f}")
        print(f"Recall@3: {metrics['recall']:.2f}")
        print(f"Accuracy@3: {metrics['accuracy']:.2f}")

    # save results    
    output_path = "output_files/evaluation_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
