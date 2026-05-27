import faiss

# LOAD FAISS INDEX

index = faiss.read_index(

    "faiss_index.bin"
)

# TOTAL VECTORS


print(f" TOTAL VECTORS: {index.ntotal}")

# SHOW ALL VECTORS

for i in range(index.ntotal):

    vector = index.reconstruct(i)

    print(f"\n VECTOR {i + 1}")

    print("\n-----------------------------------")

    print(vector)

    print("\n===================================")