import os
import pickle

import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from engines.azure_config import (
    client_azure
)

# EMBEDDING MODEL

embedding_model = SentenceTransformer(

    "all-MiniLM-L6-v2"
)

print("Embedding Model Loaded!")

# BASE DIRECTORY

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# RAG DATA PATH

RAG_PATH = os.path.join(

    BASE_DIR,
    "..",
    "rag_data"
)

# LOAD FAISS INDEX

FAISS_INDEX_PATH = os.path.join(

    RAG_PATH,
    "faiss_index.bin"
)

index = faiss.read_index(

    FAISS_INDEX_PATH
)

print("FAISS Index Loaded!")

# LOAD CHUNKS

CHUNKS_PATH = os.path.join(

    RAG_PATH,
    "chunks.pkl"
)

with open(

    CHUNKS_PATH,

    "rb"

) as f:

    chunks = pickle.load(f)

print("Chunks Loaded!")

# POLICY SEARCH

def policy_rag_search(query):

    query_embedding = embedding_model.encode(

        [query]
    )

    query_embedding = np.array(

        query_embedding

    ).astype("float32")

    distances, indices = index.search(

        query_embedding,

        3
    )

    retrieved_docs = [

        chunks[i]

        for i in indices[0]
    ]

    context = "\n".join(

        retrieved_docs
    )[:1200]

    response = client_azure.chat.completions.create(

        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),

        timeout=15,

        messages=[

            {
                "role": "system",

                "content":
                """
                You are an enterprise
                policy assistant.

                IMPORTANT RULES:

                - Answer ONLY using context
                - No fake information

                FORMAT RULES:

                Result:
                Key Findings:
                Insights:
                """
            },

            {
                "role": "user",

                "content":
                f"""

                Context:
                {context}

                Question:
                {query}

                """
            }
        ]
    )

    return (

        response
        .choices[0]
        .message
        .content
    )