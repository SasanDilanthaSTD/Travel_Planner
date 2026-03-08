import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

load_dotenv()

flight_agent = Agent(
    name="Flight_Agent",
    model="gemini-2.5-flash",
    description="Finds flight options for a destination and date",
    tools=[google_search]
)

async def run_agent():
    runner = InMemoryRunner(
        agent=flight_agent
    )
    event = await runner.run_debug("Find me a flight from UAE to Paris next month under $500.")
    
if __name__ == "__main__":
    asyncio.run(
        run_agent()
    )