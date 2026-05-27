import os

from logger_config import logger

from engines.azure_config import (
    client_azure
)

# MAIN ROUTER FUNCTION

def keyword_route(query):

    normalized_query = query.lower()

    retail_keywords = [
        "sale",
        "sales",
        "revenue",
        "store",
        "stores",
        "retail",
        "pricing",
        "customer",
        "weekly_sales",
        "top 5"
    ]

    inventory_keywords = [
        "inventory",
        "stock",
        "warehouse",
        "supply",
        "demand",
        "forecast"
    ]

    policy_keywords = [
        "policy",
        "attendance",
        "compliance",
        "hr",
        "cybersecurity",
        "governance"
    ]

    if any(keyword in normalized_query for keyword in retail_keywords):
        return "Retail Strategy Agent"

    if any(keyword in normalized_query for keyword in inventory_keywords):
        return "Inventory Optimization Agent"

    if any(keyword in normalized_query for keyword in policy_keywords):
        return "Policy Compliance Agent"

    return None

def route_query(query):

    try:

        # LOG USER QUERY

        logger.info(

            f"User Query: {query}"
        )

        selected_agent = keyword_route(query)

        if selected_agent is None:

            # AZURE ROUTER

            router_response = client_azure.chat.completions.create(

                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),

                temperature=0,

                messages=[

                    {
    "role": "system",

    "content":
    """
    You are an enterprise AI router.

    Your job is to route ONLY Walmart
    enterprise-related queries.

    VALID AGENTS:

    1. Retail Strategy Agent
       - store sales
       - retail analytics
       - pricing
       - revenue
       - customer trends

    2. Inventory Optimization Agent
       - stock
       - inventory
       - supply chain
       - warehouse
       - demand forecasting

    3. Policy Compliance Agent
       - company policy
       - HR policy
       - compliance
       - cybersecurity policy
       - governance documents

    IMPORTANT:

    Block:
    - general knowledge questions
    - politics
    - celebrities
    - sports
    - geography
    - coding help
    - unrelated questions

    VALID OUTPUTS ONLY:

    Retail Strategy Agent
    Inventory Optimization Agent
    Policy Compliance Agent
    Blocked Query

    Return ONLY one output.
    """
},

                    {
                        "role": "user",

                        "content": query
                    }
                ]
            )

            selected_agent = (

                router_response
                .choices[0]
                .message
                .content
                .strip()
            )

        # LOG SELECTED AGENT

        logger.info(

            f"Selected Agent: {selected_agent}"
        )

        print(f"\n Selected Agent: {selected_agent}")

        # RETAIL AGENT

        if selected_agent == "Retail Strategy Agent":

            logger.info(

                "Executing Retail Strategy Agent"
            )

            from engines.pandas_ai_engine import retail_analysis

            response = retail_analysis(query)

            logger.info(

                "Retail Strategy Agent Completed"
            )

            return {

                "agent":
                selected_agent,

                "response":
                response
            }

        # INVENTORY AGENT

        elif selected_agent == "Inventory Optimization Agent":

            logger.info(

                "Executing Inventory Optimization Agent"
            )

            from engines.pandas_ai_engine import inventory_analysis

            response = inventory_analysis(query)

            logger.info(

                "Inventory Optimization Agent Completed"
            )

            return {

                "agent":
                selected_agent,

                "response":
                response
            }

        # POLICY AGENT

        elif selected_agent == "Policy Compliance Agent":

            logger.info(

                "Executing Policy Compliance Agent"
            )

            from engines.rag_engine import policy_rag_search

            response = policy_rag_search(query)

            logger.info(

                "Policy Compliance Agent Completed"
            )

            return {

                "agent":
                selected_agent,

                "response":
                response
            }

        # DEFAULT BLOCK

        else:

            logger.warning(

                f"Blocked Query: {query}"
            )

            return {

                "agent":
                "Blocked Query",

                "response":
                """I’m sorry, but this system is optimize for Walmart enterprise analytics queries."""
            }

    except Exception as e:

        # LOG ERROR

        logger.error(

            f"Router Error: {str(e)}"
        )

        return {

            "agent":
            "Agent Router Error",

            "response":
            f" Error: {str(e)}"
        }
