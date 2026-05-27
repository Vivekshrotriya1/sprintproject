import pandas as pd

from pandasai import Agent as PandasAgent

from engines.azure_config import llm

from engines.response_formatter import (
    format_business_response
)

# LOAD DATASET

import os

# BASE DIRECTORY

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# DATASET PATH

DATASET_PATH = os.path.join(

    BASE_DIR,
    "..",
    "..",
    "data",
    "processed",
    "cleaned_walmart_dataset.csv"
)

# LOAD DATASET

df = pd.read_csv(

    DATASET_PATH
)

print("Dataset Loaded Successfully!")


# PANDASAI AGENT

pandas_agent = PandasAgent(

    df,

    config={

        "llm": llm,

        "verbose": False,

        "save_logs": False,

        "enable_cache": False,

        "save_charts": False,

        "open_charts": False,

        "use_error_correction_framework": True,

        "custom_whitelisted_dependencies": [

            "pandas",

            "numpy"
        ]
    }
)

print("PandasAI Agent Ready!")

# SAFE QUERY

def safe_pandas_query(query):

    return f"""

    Use ONLY pandas dataframe operations.

    IMPORTANT RULES:

    - Do NOT use imports
    - Do NOT use matplotlib
    - Do NOT use external libraries
    - Do NOT generate fake columns
    - Use ONLY dataframe analysis
    - Return concise analytical answers

    Query:
    {query}

    """

# RETAIL ANALYSIS

def retail_analysis(query):

    raw_result = str(

        pandas_agent.chat(

            safe_pandas_query(query)
        )
    )

    final_response = format_business_response(

        query=query,

        raw_result=raw_result,

        agent_type="Retail Strategy"
    )

    return final_response

# INVENTORY ANALYSIS

def inventory_analysis(query):

    inventory_query = f"""

    Analyze this query from an inventory
    and supply chain perspective.

    Focus on:

    - inventory demand
    - stock optimization
    - high-demand stores
    - inventory forecasting
    - supply chain efficiency

    Query:
    {query}

    """

    raw_result = str(

        pandas_agent.chat(

            safe_pandas_query(
                inventory_query
            )
        )
    )

    final_response = format_business_response(

        query=query,

        raw_result=raw_result,

        agent_type="Inventory Optimization"
    )

    return final_response