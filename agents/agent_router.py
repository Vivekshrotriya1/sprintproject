import os

from crewai import (

    Agent,

    Task,

    Crew,

    Process
)

from logger_config import logger

from engines.azure_config import (
    client_azure
)

from engines.pandas_ai_engine import (

    retail_analysis,

    inventory_analysis
)

from engines.rag_engine import (
    policy_rag_search
)

# RETAIL AGENT

retail_agent = Agent(

    role="Retail Strategy Expert",

    goal="""
    Analyze Walmart retail sales,
    store performance,
    and business KPIs.
    """,

    backstory="""
    Enterprise retail analytics expert.
    """,

    verbose=True,

    allow_delegation=False
)

# INVENTORY AGENT

inventory_agent = Agent(

    role="Inventory Optimization Expert",

    goal="""
    Analyze inventory demand,
    warehouse performance,
    and supply chain optimization.
    """,

    backstory="""
    Enterprise inventory analytics expert.
    """,

    verbose=True,

    allow_delegation=False
)

# POLICY AGENT

policy_agent = Agent(

    role="Policy Compliance Expert",

    goal="""
    Answer enterprise policy
    and compliance queries.
    """,

    backstory="""
    Enterprise compliance and
    governance specialist.
    """,

    verbose=True,

    allow_delegation=False
)

# MAIN ROUTER FUNCTION

def route_query(query):

    try:

        # LOG USER QUERY

        logger.info(

            f"User Query: {query}"
        )

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

            task = Task(

                description=f"""
                Analyze retail query:

                {query}
                """,

                expected_output="""
                Retail analytics insights.
                """,

                agent=retail_agent
            )

            crew = Crew(

                agents=[retail_agent],

                tasks=[task],

                process=Process.sequential,

                verbose=True
            )

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

            task = Task(

                description=f"""
                Analyze inventory query:

                {query}
                """,

                expected_output="""
                Inventory optimization insights.
                """,

                agent=inventory_agent
            )

            crew = Crew(

                agents=[inventory_agent],

                tasks=[task],

                process=Process.sequential,

                verbose=True
            )

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

            task = Task(

                description=f"""
                Analyze policy query:

                {query}
                """,

                expected_output="""
                Enterprise policy response.
                """,

                agent=policy_agent
            )

            crew = Crew(

                agents=[policy_agent],

                tasks=[task],

                process=Process.sequential,

                verbose=True
            )

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
            "CrewAI Router Error",

            "response":
            f" Error: {str(e)}"
        }