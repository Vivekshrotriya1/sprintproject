import faiss
import pickle
import numpy as np
import os

from pypdf import PdfReader

from sentence_transformers import (
    SentenceTransformer
)

# PDF PATH

pdf_path = "../documents/policy.pdf"

# EXTRACT TEXT

all_text = ""

reader = PdfReader(pdf_path)

for page in reader.pages:

    text = page.extract_text()

    if text:

        all_text += text + "\n"

print("Text Extraction Completed!")

# TEXT CHUNKING

chunk_size = 500

chunks = [

    all_text[i:i + chunk_size]

    for i in range(
        0,
        len(all_text),
        chunk_size
    )
]

print(f"Total Chunks: {len(chunks)}")

# LOAD EMBEDDING MODEL

embedding_model = SentenceTransformer(

    "all-MiniLM-L6-v2"
)

print("Embedding Model Loaded!")

# CREATE EMBEDDINGS

embeddings = embedding_model.encode(

    chunks
)

embeddings = np.array(

    embeddings
).astype("float32")

print("Embeddings Created!")

# CREATE FAISS INDEX

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(

    dimension
)

index.add(embeddings)

print("FAISS Index Created!")

# SAVE INDEX

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FAISS_INDEX_PATH = os.path.join(

    BASE_DIR,
    "faiss_index.bin"
)

faiss.write_index(

    index,

    FAISS_INDEX_PATH
)

# SAVE CHUNKS

CHUNKS_PATH = os.path.join(

    BASE_DIR,
    "chunks.pkl"
)

with open(

    CHUNKS_PATH,

    "wb"

) as f:

    pickle.dump(chunks, f)



print("FAISS DATABASE CREATED!")
