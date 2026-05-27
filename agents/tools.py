import pandas as pd

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from openai import AzureOpenAI

from dotenv import load_dotenv

import os

load_dotenv()

# ======================================
# AZURE OPENAI CLIENT
# ======================================

client_azure = AzureOpenAI(

    api_key=os.getenv(
        "AZURE_OPENAI_API_KEY"
    ),

    api_version=os.getenv(
        "AZURE_OPENAI_API_VERSION"
    ),

    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)

# ======================================
# LOAD DATASET
# ======================================

df = pd.read_csv(

    "../data/processed/cleaned_walmart_dataset.csv"
)

print("\n✅ Dataset Loaded Successfully!")

# ======================================
# RETAIL STRATEGY TOOL
# ======================================

def retail_strategy_tool(query):

    total_sales = round(
        df['Weekly_Sales'].sum(),
        2
    )

    avg_sales = round(
        df['Weekly_Sales'].mean(),
        2
    )

    best_store = df.groupby(
        'Store'
    )['Weekly_Sales'].sum().idxmax()

    top_department = df.groupby(
        'Dept'
    )['Weekly_Sales'].sum().idxmax()

    context = f"""

    Walmart Retail Dataset Insights:

    Total Sales:
    {total_sales}

    Average Weekly Sales:
    {avg_sales}

    Best Store:
    {best_store}

    Top Department:
    {top_department}

    """

    response = client_azure.chat.completions.create(

        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),

        messages=[

            {
                "role": "system",

                "content":
                """
                You are a retail strategy AI assistant.

                Analyze Walmart business data
                and answer user questions intelligently.
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

    return response.choices[0].message.content

# ======================================
# INVENTORY OPTIMIZATION TOOL
# ======================================

def inventory_optimization_tool(query):

    holiday_sales = df.groupby(
        'IsHoliday'
    )['Weekly_Sales'].mean()

    non_holiday_sales = round(
        holiday_sales[0],
        2
    )

    holiday_sales_avg = round(
        holiday_sales[1],
        2
    )

    sales_difference = round(
        holiday_sales_avg - non_holiday_sales,
        2
    )

    context = f"""

    Walmart Inventory Insights:

    Average Non-Holiday Sales:
    {non_holiday_sales}

    Average Holiday Sales:
    {holiday_sales_avg}

    Sales Increase During Holidays:
    {sales_difference}

    """

    response = client_azure.chat.completions.create(

        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),

        messages=[

            {
                "role": "system",

                "content":
                """
                You are an enterprise inventory
                optimization AI assistant.

                Answer inventory, demand forecasting,
                warehouse, and supply chain questions
                intelligently using provided context.
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

    return response.choices[0].message.content

# ======================================
# LOAD EMBEDDING MODEL
# ======================================

embedding_model = SentenceTransformer(

    "all-MiniLM-L6-v2"
)

print("\n✅ Embedding Model Loaded!")

# ======================================
# CHROMADB CLIENT
# ======================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "vector_store"
)

print(f"\n📂 Vector DB Path: {VECTOR_DB_PATH}")

client_chroma = chromadb.PersistentClient(

    path=VECTOR_DB_PATH
)

# ======================================
# LOAD COLLECTION
# ======================================

try:

    collection = client_chroma.get_collection(

        name="retail_docs"
    )

    print("\n✅ Vector Database Connected!")

except Exception as e:

    print(f"""

    ❌ ChromaDB Collection Error:

    {str(e)}

    Run:
    python rag_setup.py

    """)

    collection = None

# ======================================
# POLICY SEARCH TOOL (RAG)
# ======================================

def policy_search_tool(query):

    if collection is None:

        return """

        ❌ Vector database not found.

        Please run:
        python rag_setup.py

        """

    try:

        # ======================================
        # CREATE QUERY EMBEDDING
        # ======================================

        query_embedding = embedding_model.encode(
            query
        ).tolist()

        # ======================================
        # SEARCH VECTOR DATABASE
        # ======================================

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=3
        )

        retrieved_docs = results["documents"][0]

        context = "\n".join(retrieved_docs)

        # ======================================
        # AZURE OPENAI RESPONSE
        # ======================================

        response = client_azure.chat.completions.create(

            model=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT"
            ),

            messages=[

                {
                    "role": "system",

                    "content":
                    """
                    You are an enterprise retail
                    policy assistant.

                    Answer ONLY using
                    provided context.

                    If answer is not found,
                    say:
                    'Information not found
                    in enterprise documents.'

                    Do not generate fake information.
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

        return response.choices[0].message.content

    except Exception as e:

        return f"""

        ❌ Error in Policy Agent:

        {str(e)}

        """