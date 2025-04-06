import streamlit as st
from agents.ollama_agent import OllamaAgent
from pydantic import BaseModel
import asyncio 

class FreeFormResponse(BaseModel):
    content: str

# Initialize the Ollama agent
agent = OllamaAgent(
    model_name="llama3.2:3b-instruct-fp16",
    base_url="http://localhost:11434/v1",
)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Streamlit UI
st.title("💬 Chat with Ollama Agent")
st.caption("🚀 A chatbot powered by Ollama Agent")

# Display conversation history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box for user query at the bottom
if user_query := st.chat_input("Type your message here..."):
    # Add user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # Agent response
    with st.spinner("Agent is thinking..."):
        try:
            # Run the agent and get the result
            result = asyncio.run(agent.run(user_query))
            
            # Extract the 'content' field from the JSON response
            response_content = result.data  # Assuming result.data is parsed into FreeFormResponse

            # Add agent response to session state
            st.session_state["messages"].append({"role": "assistant", "content": response_content})
            st.chat_message("assistant").write(response_content)

        except Exception as e:
            error_message = f"An error occurred: {e}"
            st.session_state["messages"].append({"role": "assistant", "content": error_message})
            st.chat_message("assistant").write(error_message)