from typing import Dict, Any
import uuid
from datetime import datetime
from app.agents.graph import graph_agent  # Import the compiled graph

# Import agent functions directly (not as classes)
from app.agents.query_agent import query_agent
from app.agents.data_agent import data_agent
from app.agents.analysis_agent import analysis_agent


class AgentService:
    def __init__(self):
        """Initialize the AgentService with all required agents."""
        # No need to store agent instances as they are functions
        pass

    async def process_message(
        self,
        user_message: str,
        thread_id: str,
    ) -> Dict[str, Any]:
        """
        Process a user message through the agent pipeline.

        Args:
            user_message: The user's input message
            thread_id: Unique identifier for the conversation thread

        Returns:
            Dictionary containing the agent's response and metadata
        """
        try:
            state = {"messages": [{"role": "user", "content": user_message}]}

            query_result = query_agent(state)
            decision = query_result.get("decision", "unknown")

            if decision == "data":
                agent_response = data_agent(state)
                response_type = "data"
            else:  # Default to analysis
                agent_response = analysis_agent(state)
                response_type = "analysis"

            response_state = {
                "messages": state["messages"]
                + [
                    {
                        "role": "ai",
                        "content": f"Processing with {response_type} agent...",
                    },
                    {"role": "user", "content": user_message},
                ]
            }
            try:
                result = await graph_agent.ainvoke(response_state)
            except Exception as e:
                error_msg = f"Error processing message: {str(e)}"
            final_message = result.get("messages", [{}])[-1].get(
                "content", "No response generated"
            )

            return {
                "response_id": str(uuid.uuid4()),
                "message": final_message,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "thread_id": thread_id,
                    # Add any additional metadata from the graph execution
                },
            }

        except Exception as e:
            # Log the error and re-raise with more context
            error_msg = f"Error processing message: {str(e)}"
            print(error_msg)
            raise Exception(error_msg) from e
