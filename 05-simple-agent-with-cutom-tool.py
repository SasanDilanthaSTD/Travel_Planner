import asyncio
import requests
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool

load_dotenv()

# 1. Custom tool to call Open-Meteo API to get weather data (no API key needed)
def get_weather(coords:dict) -> dict:
    """
    Args:
        coords (dict): {"lat": float, "lon": float}

    Returns:
        dict: JSON weather data from Open-Meteo API
    """
    lat = coords.get("lat")
    lon = coords.get("lon")
    
    if lat is None or lon is None:
        return {"error": "Invalid coordinates. 'lat' and 'lon' are required."}
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

weather_tool = FunctionTool(get_weather)

# 2. Define agent with the custom tool
flight_agent = Agent(
    name="Flight_Agent",
    model="gemini-2.5-flash",
    description="yoU Are a flight assistant. Use get_weather tool to provide current weather information for a location.",
    instruction="""
        You are a travel assistant.
        - If user ask about weather in a location (latitude/longitude), call get_weather tool.
        - otherwise, respond appropriately.
        When returning weather, report temperature, wind speed and other available data.
    """,
    tools=[weather_tool]
)
    
async def run_agent():
    runner = InMemoryRunner(agent=flight_agent)
    query = "What is the current weather at Dubai. lat: 25.2048, lon: 55.2708?"
    event = await runner.run_debug(query)
    
if __name__ == "__main__":
    asyncio.run(run_agent())
    