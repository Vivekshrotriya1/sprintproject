from engines.azure_config import client_azure

import os

# FORMAT RESPONSE

def format_business_response(

    query,
    raw_result,
    agent_type
):

    response = client_azure.chat.completions.create(

        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),

        messages=[

            {
                "role": "system",

                "content":
                f"""
                You are an enterprise
                {agent_type} assistant.

                FORMAT RULES:

                Result:
                Key Findings:
                Insights:

                IMPORTANT:

                - Keep response concise
                - No recommendations
                - No markdown tables
                """
            },

            {
                "role": "user",

                "content":
                f"""

                Query:
                {query}

                Raw Result:
                {raw_result}

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