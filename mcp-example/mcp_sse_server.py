from datetime import datetime
from random import choice, randint

from mcp.server.fastmcp import FastMCP

app = FastMCP(name="demo-info", instructions="Dummy weather and traffic data.")


@app.tool(description="Get dummy weather for a city.")
def get_weather(city: str = "San Francisco") -> dict:
    conditions = ["sunny", "overcast", "light rain", "windy", "foggy"]
    return {
        "city": city,
        "observed_at_utc": datetime.now().isoformat() + "Z",
        "temperature_c": randint(8, 28),
        "condition": choice(conditions),
    }


@app.tool(description="Get dummy traffic info for a route.")
def get_traffic(route: str = "US-101 at Marsh Rd") -> dict:
    congestion = ["clear", "slowing", "heavy", "gridlock"]
    return {
        "route": route,
        "reported_at_utc": datetime.now().isoformat() + "Z",
        "congestion": choice(congestion),
        "estimated_delay_minutes": randint(0, 25),
    }

# HTTP (SSE) entrypoint
if __name__ == "__main__":
    import uvicorn

    print("Starting FastMCP demo server (SSE) on http://127.0.0.1:8000")

    uvicorn.run(
        app.sse_app(),   # <-- this is the supported HTTP mode in FastMCP
        host="127.0.0.1",
        port=8000,
    )

# Run MCP inspector to test: npx @modelcontextprotocol/inspector

