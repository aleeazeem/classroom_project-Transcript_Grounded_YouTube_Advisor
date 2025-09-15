import argparse
from src.utils.retriever import Retriever
from src.utils.chat_utils import ChatUtils

def main():
    parser = argparse.ArgumentParser(description="Ask a question to ChromaDB + OpenAI")
    parser.add_argument("question", type=str, help="The question you want to ask")
    parser.add_argument("--k", type=int, default=3, help="Number of results to retrieve")
    args = parser.parse_args()

    # Initialize classes
    retriever = Retriever()
    chat_utils = ChatUtils()

    # Get chunks from Chroma
    chunks = retriever.query(args.question, args.k)

    if not chunks:
        print("⚠️ No results found in ChromaDB.")
        return

    # Take the top result
    top_chunk = chunks[0]
    rephrased = chat_utils.rephrase(top_chunk["clean_text"], top_chunk)

    print("\n💡 Answer:")
    print(rephrased)


if __name__ == "__main__":
    main()
