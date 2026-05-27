import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from engines.azure_config import client_azure


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RAG_PATH = os.path.join(
    BASE_DIR,
    "..",
    "rag_data"
)

CHUNKS_PATH = os.path.join(
    RAG_PATH,
    "chunks.pkl"
)

chunks = None
vectorizer = None
chunk_matrix = None


def load_policy_index():
    global chunks, vectorizer, chunk_matrix

    if chunks is not None:
        return

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    chunk_matrix = vectorizer.fit_transform(chunks)


def retrieve_policy_context(query, top_k=3):
    load_policy_index()

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, chunk_matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_k]

    return "\n".join(
        chunks[index]
        for index in top_indices
        if scores[index] > 0
    )[:1200]


def policy_rag_search(query):
    context = retrieve_policy_context(query)

    if not context:
        return "No relevant policy context found."

    response = client_azure.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        timeout=15,
        messages=[
            {
                "role": "system",
                "content": """
                You are an enterprise policy assistant.

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
                "content": f"""
                Context:
                {context}

                Question:
                {query}
                """
            }
        ]
    )

    return response.choices[0].message.content
