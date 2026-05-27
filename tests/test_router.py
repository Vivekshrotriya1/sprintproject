import sys
import os


# PROJECT ROOT


CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        ".."
    )
)


# AGENTS PATH


AGENTS_PATH = os.path.join(

    PROJECT_ROOT,

    "agents"
)

sys.path.append(AGENTS_PATH)


# IMPORT ROUTER


from agent_router import (
    route_query
)


# RETAIL TEST


def test_retail_agent():

    response = route_query(

        "top 5 stores sales"
    )

    assert response["agent"] == (
        "Retail Strategy Agent"
    )


# INVENTORY TEST


def test_inventory_agent():

    response = route_query(

        "high demand inventory"
    )

    assert response["agent"] == (
        "Inventory Optimization Agent"
    )


# POLICY TEST


def test_policy_agent():

    response = route_query(

        "What is attendance policy?"
    )

    assert response["agent"] == (
        "Policy Compliance Agent"
    )


# BLOCKED TEST


def test_blocked_query():

    response = route_query(

        "Who won IPL 2025?"
    )

    assert response["agent"] == (
        "Blocked Query"
    )