import os

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from pypdf import PdfReader

# ======================================
# PDF FOLDER PATH
# ======================================

pdf_folder = "documents"

# ======================================
# GET ALL PDF FILES
# ======================================

pdf_files = [

    os.path.join(pdf_folder, file)

    for file in os.listdir(pdf_folder)

    if file.endswith(".pdf")
]

print("\n📄 PDFs Found:\n")

for pdf in pdf_files:

    print(pdf)

# ======================================
# EXTRACT TEXT FROM PDFs
# ======================================

all_text = ""

for pdf in pdf_files:

    reader = PdfReader(pdf)

    for page in reader.pages:

        text = page.extract_text()

        if text:

            all_text += text + "\n"

print("\n✅ Text Extraction Completed!")

# ======================================
# TEXT CHUNKING
# ======================================

chunk_size = 1000

chunks = [

    all_text[i:i + chunk_size]

    for i in range(
        0,
        len(all_text),
        chunk_size
    )
]

print(f"\n✅ Total Chunks Created: {len(chunks)}")

# ======================================
# LOAD EMBEDDING MODEL
# ======================================

embedding_model = SentenceTransformer(

    "all-MiniLM-L6-v2"
)

print("\n✅ Embedding Model Loaded!")

# ======================================
# CREATE CHROMADB CLIENT
# ======================================

client = chromadb.PersistentClient(

    path="vector_store"
)

# ======================================
# DELETE OLD COLLECTION
# ======================================

try:

    client.delete_collection(
        name="retail_docs"
    )

    print("\n🗑️ Old Collection Deleted!")

except:

    print("\n⚠️ No Old Collection Found!")

# ======================================
# CREATE NEW COLLECTION
# ======================================

collection = client.get_or_create_collection(

    name="retail_docs"
)

print("\n✅ New Collection Created!")

# ======================================
# STORE EMBEDDINGS
# ======================================

for idx, chunk in enumerate(chunks):

    embedding = embedding_model.encode(
        chunk
    ).tolist()

    collection.add(

        ids=[str(idx)],

        embeddings=[embedding],

        documents=[chunk]
    )

print("\n===================================")

print("✅ VECTOR DATABASE CREATED SUCCESSFULLY")

print("===================================")

print(f"📄 Total PDFs Processed: {len(pdf_files)}")

print(f"📦 Total Chunks Stored: {len(chunks)}")