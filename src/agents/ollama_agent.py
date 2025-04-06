from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
from pydantic_ai.mcp import MCPServerHTTP
import logging
import streamlit as st


class OllamaAgent:
    mcp_server = MCPServerHTTP(url='http://localhost:4000/sse') 
    def __init__(self, model_name: str, base_url: str):
        self.model = OpenAIModel(model_name=model_name, provider=OpenAIProvider(base_url=base_url))
        self.agent = Agent(
            self.model,
            system_prompt=(
                "You are chat bot assistant."
                "You can use available tools to help users when required."
            ),
            mcp_servers=[self.mcp_server],
        )
    async def run(self, query: str):
        async with self.agent.run_mcp_servers():
            result = await self.agent.run(query)
        return result