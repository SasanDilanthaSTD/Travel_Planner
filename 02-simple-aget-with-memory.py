from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai.types import Content, Part

import asyncio
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# 01. Create an agent: optimally give it a memory-tool for recall
agent = LlmAgent(
    name="Flight_Agent",
    model="gemini-2.5-flash",
    description="""
        Your departure is [departure].
        Tell me the optimal route between flights.
    """,
    tools=[PreloadMemoryTool()]
)

# 02. Create a runner (it creates a its owns in-memory service)
runner = InMemoryRunner(
    agent=agent,
    app_name="flight_app_agent"
)

async def run_dialogue():
    # First session: user gives some info
    session_id = "session_1"
    
    # Create the first session 
    await runner.session_service.create_session(
        app_name=runner.app_name,
        session_id=session_id,
        user_id="user_1"
    )
    user_query = "I am traveling to Tokyo"
    print(f"User: {user_query}")
    content = Content(role="user", parts=[Part(text=user_query)])
    
    async for event in runner.run_async(
        user_id="user_1",
        session_id=session_id,
        new_message=content
    ):
        # Check if event has content and is from agent(not user)
        if event.content and event.content.parts and event.author != "user_1":
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")
                    
    # After conversation, save to memory
    session = await runner.session_service.get_session(
        app_name=runner.app_name,
        session_id=session_id,
        user_id="user_1"
    )
    await runner.memory_service.add_session_to_memory(session=session)
    
    print("\n--- ")
    print(f"User: Where am I traveling?")
    content = Content(role="user", parts=[Part(text="Where am I traveling?")])
    async for event in runner.run_async(
        user_id="user_1",
        session_id=session_id,
        new_message=content
    ):
        if event.content and event.content.parts and event.author != "user_1":
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")
    
    
if __name__ == "__main__":
    asyncio.run(run_dialogue())
    

