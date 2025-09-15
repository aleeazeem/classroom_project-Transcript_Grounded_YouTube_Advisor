# Transcript_Grounded_YouTube_Advisor

## Overview

Description:
Build a small but production-minded chatbot that gives creators practical advice on how to improve their YouTube channel, grounded only in two provided video transcripts.  Answers must include citations pointing to the specific video(s) and timestamp ranges used to generate the advice when applicable.
A transcripts/ folder containing two ~1-hour transcripts about YouTube channel growth, each with timestamps and basic metadata.

- aprilynne.txt This video is about improving video introductions.
- hayden.txt This video is about improving storytelling.

## Instrcutions
Run requirements.txt file
Run requirements-dev.txt file
There are two steps to execute the project
### Run dvc pipeline 
   Run [dvc.yaml](https://github.com/aleeazeem/classroom_project-Transcript_Grounded_YouTube_Advisor/blob/main/dvc.yaml) file using following two command
    $dvc init
       -  initalize the dvc pipeline
    $dvc repro
       - that will perform 
        ⬇ ingestion (using introduction.yaml / storytelling.yaml) 
        ⬇ preprocessing (perform feature engineering and save the csv files)
        ⬇ embeddings (merge both the files into one with their respective title)
        ⬇ stored in chroma_db(embeddings will be stored in db with their respective meta data)
        ⬇ evaluation 
       - As result of run it will create following folders: chroma_db, output_files, logs
### Start using chatbot
    python src/core/chatbot.py "what makes a good youtube introduction"


Troubleshooting
    - if you see any numpy related error while running the dvc pipeline then uninstall numpy and re-install numpy==1.26.4