from langgraph.graph import StateGraph, START, END, MessagesState
from app.agents.query_agent import query_agent
from app.agents.data_agent import data_agent
from app.agents.response_agent import response_agent
from app.agents.analysis_agent import analysis_agent

graph = StateGraph(MessagesState)

# Add nodes
graph.add_node("query_agent", query_agent)
graph.add_node("data_agent", data_agent)
graph.add_node("analysis_agent", analysis_agent)
graph.add_node("response_agent", response_agent)

# Define the flow
graph.add_edge(START, "query_agent")  # Start with query_agent

# Conditional edges from query_agent
graph.add_conditional_edges(
    "query_agent",
    lambda state: state.get("decision"),
    {"data": "data_agent", "analysis": "analysis_agent", "unknown": "response_agent"},
)

# Connect data_agent and analysis_agent to response_agent
graph.add_edge("data_agent", "response_agent")
graph.add_edge("analysis_agent", "response_agent")

# End the flow after response_agent
graph.add_edge("response_agent", END)

# Compile the graph
compiled_graph = graph.compile()
graph_agent = compiled_graph
