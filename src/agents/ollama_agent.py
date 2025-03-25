from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

# Define the input model
class WeatherInput(BaseModel):
    city: str

# Define the output model
class WeatherOutput(BaseModel):
    city: str
    condition: str
    temperature: int

class WeatherAgent:
    def __init__(self, model_name: str, base_url: str):
        self.model = OpenAIModel(model_name=model_name, provider=OpenAIProvider(base_url=base_url))
        self.agent = Agent(
            self.model,
            system_prompt=(
                "You are chat bot assistant."
                "You can use available tools to help users if required."
            )
        )

        @self.agent.tool_plain
        def get_weather(data: WeatherInput) -> WeatherOutput:
            """
            Provide mock weather information for a given city.
            If real-time data is unavailable, return a polite message.
            """
            # Mock response for demonstration purposes
            return WeatherOutput(
                city=data.city,
                condition="sunny",
                temperature=33
            )

    def run(self, query: str):
        return self.agent.run_sync(query)