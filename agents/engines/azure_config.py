import os

from dotenv import load_dotenv

from openai import AzureOpenAI as AzureClient

from pandasai.llm.azure_openai import AzureOpenAI

load_dotenv()

# AZURE OPENAI CLIENT

client_azure = AzureClient(

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

# PANDASAI LLM

llm = AzureOpenAI(

    api_token=os.getenv(
        "AZURE_OPENAI_API_KEY"
    ),

    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    ),

    api_version=os.getenv(
        "AZURE_OPENAI_API_VERSION"
    ),

    deployment_name=os.getenv(
        "AZURE_OPENAI_DEPLOYMENT"
    )
)