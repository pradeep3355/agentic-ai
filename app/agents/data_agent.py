from langgraph.graph import MessagesState


def data_agent(state: MessagesState):
    return {
        "messages": [
            {
                "role": "ai",
                "content": "DataAgent: Fetched and processed the required data.",
            }
        ],
        "result": "Data fetched successfully",
    }
