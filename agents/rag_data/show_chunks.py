import pickle

# LOAD CHUNKS FILE

with open(

    "chunks.pkl",

    "rb"

) as f:

    chunks = pickle.load(f)

# TOTAL CHUNKS



print(f" TOTAL CHUNKS: {len(chunks)}")

# SHOW ALL CHUNKS

for idx, chunk in enumerate(chunks):

    print(f"\n CHUNK {idx + 1}")


    print(chunk)

