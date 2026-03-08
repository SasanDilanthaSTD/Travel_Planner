import os 
from dotenv import load_dotenv
import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

load_dotenv()

flight_agent = Agent(
    name="Flight_Agent",
    model="gemini-2.5-flash",
    description="Tell me the optimal route between the flight"
)


async def run_agent():
    runner = InMemoryRunner(
        agent=flight_agent
    )
    events = await runner.run_debug(
        "How many layovers are there between New York and Tokyo?"
    )
    
if __name__ == "__main__":
    asyncio.run(run_agent())