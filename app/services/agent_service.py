from typing import Dict, Any
import uuid
from datetime import datetime, timezone
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

                # Handle different message formats
                messages = result.get("messages", [])
                print(f"Messages from graph_agent: {messages}")  # Debug log

                if not messages:
                    final_message = "No response generated"
                else:
                    last_message = messages[-1]
                    print(f"Last message type: {type(last_message)}")  # Debug log

                    try:
                        # Handle LangChain's HumanMessage/AIMessage objects
                        if hasattr(last_message, "content"):
                            final_message = last_message.content
                        # Handle dictionary format
                        elif isinstance(last_message, dict):
                            final_message = last_message.get(
                                "content", str(last_message)
                            )
                        # Handle string or any other type
                        else:
                            final_message = str(last_message)

                    except Exception as e:
                        error_msg = f"Error extracting message content: {str(e)}"
                        print(error_msg)
                        final_message = (
                            "An error occurred while processing the response"
                        )

            except Exception as e:
                error_msg = f"Error processing message: {str(e)}"
                print(f"Error details: {error_msg}")
                final_message = "An error occurred while processing your request"

            return {
                "response_id": str(uuid.uuid4()),
                "message": final_message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
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
