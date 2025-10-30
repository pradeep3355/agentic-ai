from langgraph.graph import MessagesState


def analysis_agent(state: MessagesState):
    return {
        "messages": [
            {
                "role": "ai",
                "content": "AnalysisAgent: Performed analysis on the given input.",
            }
        ],
        "result": "Analysis completed successfully",
    }
