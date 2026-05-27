from fastapi import APIRouter

from pydantic import BaseModel

import sys
import os

# ADD AGENTS FOLDER PATH

sys.path.append(

    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../agents"
        )
    )
)


router = APIRouter()

# REQUEST MODEL

class ChatRequest(BaseModel):

    query: str

# AGENT CHAT API

@router.post("/agent-chat")

def agent_chat(request: ChatRequest):

    try:

        from agent_router import route_query

        result = route_query(

            request.query
        )

        return {

            "query":
            request.query,

            "selected_agent":
            result["agent"],

            "response":
            result["response"]
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }
