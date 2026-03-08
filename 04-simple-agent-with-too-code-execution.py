import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.code_executors import BuiltInCodeExecutor

load_dotenv()

flight_agent = Agent(
    name="Flight_Agent",
    model="gemini-2.5-flash",
    description="Finds flight options or compute flight related data using code execution",
    instruction="""
        You are the flight helper agent.
        If ther user want to perform computation (eg. calculate the duration of flight, time difference between two cities etc.) 
        generate Python code inside ````python ... ```` blocks.
        The code will be executed automatically and results returned.
    """,
    code_executor=BuiltInCodeExecutor()
)

async def run_agent():
    runner = InMemoryRunner(agent=flight_agent)
    query = "Calculate how many hours between 2025-12-15 10:00 UTC and 2025-12-16 02:00 UTC (flight duration test)."
    event = await runner.run_debug(query)
    
if __name__ == "__main__":
    asyncio.run(run_agent())