from tools import policy_search_tool

# ======================================
# POLICY COMPLIANCE AGENT
# ======================================

def policy_agent():

    print("\n===================================")

    print("📄 POLICY COMPLIANCE AGENT")

    print("===================================")

    while True:

        query = input(

            "\nAsk Question (type exit to stop): "
        )

        if query.lower() == "exit":

            print("\n✅ Exiting Policy Agent")

            break

        result = policy_search_tool(query)

        print("\n🤖 ANSWER:\n")

        print(result)