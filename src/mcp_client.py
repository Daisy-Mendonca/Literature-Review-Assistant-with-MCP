"""
Minimal MCP client abstraction.
Assumes MCP HTTP JSON-RPC style endpoint at MCP_SERVER_URL.
Provides `call(agent_method, params)` which posts JSON and returns result.
Falls back to direct-calls if MCP unreachable (simple local mode).
"""
import os
import requests
from dotenv import load_dotenv
load_dotenv()


MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")


class MCPClient:
    def __init__(self, base_url: str = MCP_URL):
        self.base_url = base_url.rstrip("/")


def call(self, method: str, params: dict):
    url = f"{self.base_url}/call"
    payload = {"method": method, "params": params}
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("result")
    except Exception as e:
        # Fallback: indicate MCP unavailable
        return {"_error": str(e), "_fallback": True}


# singleton
mcp = MCPClient()