from langgraph.graph import MessagesState


def query_agent(state: MessagesState):
    user_message = state["messages"][-1]["content"].lower()

    if "data" in user_message or "fetch" in user_message:
        decision = "data"
        content = "DeciderAgent: I will call DataAgent for this task."
    elif "analyze" in user_message or "summary" in user_message:
        decision = "analysis"
        content = "DeciderAgent: I will call AnalysisAgent for this task."
    else:
        decision = "unknown"
        content = "DeciderAgent: I couldn't decide which agent to call."

    return {"decision": decision, "messages": [{"role": "ai", "content": content}]}
