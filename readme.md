# Transcript Grounded YouTube Advisor

## Overview

A production-minded chatbot that provides creators with practical advice on improving their YouTube channels, grounded exclusively in two provided video transcripts. All answers include citations pointing to specific video(s) and timestamp ranges used to generate the advice.

The system analyzes transcripts from a `transcripts/` folder containing two ~1-hour video transcripts about YouTube channel growth:

- **aprilynne.txt** - Focuses on improving video introductions
- **hayden.txt** - Focuses on improving storytelling techniques

## Prerequisites

Ensure you have Python 3.10.18 installed on your system before proceeding with the setup. There might be issues in case if you have the above version

## Installation

Install the required dependencies by running the following commands:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Usage

The project consists of two main execution steps:

### Step 1: Run DVC Pipeline

Execute the [dvc.yaml](https://github.com/aleeazeem/classroom_project-Transcript_Grounded_YouTube_Advisor/blob/main/dvc.yaml) pipeline using:

```bash
dvc init
dvc repro
```

This pipeline performs the following stages:

1. **Ingestion** - Processes transcript files using `introduction.yaml` and `storytelling.yaml` configurations
2. **Preprocessing** - Performs feature engineering and saves processed CSV files
3. **Embeddings** - Merges both transcript files with their respective titles
4. **Storage** - Stores embeddings in ChromaDB with associated metadata
5. **Evaluation** - Validates the pipeline results

Upon completion, the pipeline creates the following directories:
- `chroma_db/` - Vector database storage
- `output_files/` - Processed data files
- `logs/` - Pipeline execution logs

### Step 2: Start the Chatbot

Once the pipeline completes successfully, interact with the chatbot using:

```bash
python src/core/chatbot.py "what makes a good youtube introduction"
```

Replace the quoted text with your specific question about YouTube content creation.

## Troubleshooting

**NumPy Compatibility Issue:**
If you encounter NumPy-related errors during pipeline execution:

1. Uninstall the current NumPy version:
   ```bash
   pip uninstall numpy
   ```

2. Install the compatible version:
   ```bash
   pip install numpy==1.26.4
   ```

## Project Structure

```
CLASSROOM_PROJECT-TRANSCRIPT_GROUNDED_YOUTUBE_ADVISOR/
├── .dvc/
├── configs/
├── logs/
├── myenv/
├── output_files/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── data_ingestion.py
│   │   ├── data_preprocessing.py
│   │   ├── embedding.py
│   │   └── evaluation.py
│   └── utils/
│       ├── __pycache__/
│       ├── db_utils/
│       │   ├── embedding_db_utils.py
│       │   └── evaluation_utils.py
│       ├── __init__.py
│       ├── chat_utils.py
│       ├── common_utils.py
│       ├── data_ingestion_utils.py
│       ├── data_preprocessing_utils.py
│       ├── logger.py
│       └── retriever.py
├── transcripts/
│   ├── aprilynne.txt
│   └── hayden.txt
├── .dvcignore
├── .env
├── .gitignore
├── dvc.lock
├── dvc.yaml
├── experiment_2.ipynb
├── readme.md
├── requirements-dev.txt
└── requirements.txt
```

## Features

- **Grounded Responses**: All advice is backed by specific transcript content
- **Citation System**: Responses include video sources and timestamp references
- **Production Ready**: Built with scalability and reliability in mind
- **Vector Search**: Utilizes ChromaDB for efficient semantic search
- **Pipeline Automation**: DVC-managed data processing workflow
