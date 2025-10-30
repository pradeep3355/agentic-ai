from langgraph.graph import MessagesState


def response_agent(state: MessagesState):
    last_message = state["messages"][-1]["content"]
    return {
        "messages": [
            {
                "role": "ai",
                "content": f"ResponseAgent: Here is your final answer → {last_message}",
            }
        ]
    }
