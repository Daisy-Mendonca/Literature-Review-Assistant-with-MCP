Literature Review Assistant

1. Overview

The Literature Review Assistant is a lightweight research tool that helps users search academic papers and retrieve details using natural-language queries.

You simply type a question like:
“Find papers about contrastive learning for medical images.”

An LLM receives your query and decides which backend tool to call:
search_papers → to perform a semantic research search
get_paper_details → to fetch details for a specific paper

The project uses FastMCP as the backend tool server and a simple HTML frontend where users can type queries.
The LLM acts as an intelligent router selecting the correct tool in JSON format. This is essentially a miniature research assistant with tool-calling abilities.

--------------------------------------------------------------------

2. Key Features

MCP Tool Server (FastMCP)
    Registers Python functions as named tools on an MCP server.

Implemented tools
    search_papers(query: str, limit: int) -> list[dict]
    get_paper(paper_id: str) -> dict
    Tool implementations call Semantic Scholar APIs and return structured Python objects (JSON-serializable).

Controller (Flask)
    Exposes a single programmatic API endpoint: POST /query which accepts a JSON payload { "query": "..." }.
    Hosts the static frontend files so the entire app runs from one origin.
    Runs an LLM prompt pipeline to map natural-language queries to a structured tool invocation in JSON
    Validates and parses LLM output and enforces a strict schema before calling tools.
    Uses the FastMCP client API (SSE/HTTP transport) to call tools by name on the MCP server and forwards tool outputs to the requester.

LLM Integration
    Designed to plug in any transformer-based model (local HF model or hosted API).
    The prompt forces a JSON-only response for tool selection; controller contains parsing/fallback logic.

Frontend
    Minimal static HTML + JavaScript client that POSTs queries to /query and renders JSON results.
    Uses relative paths so it works when served from the controller (no CORS issues).
    Easily replaceable by richer UIs (React, Next.js) if desired.


--------------------------------------------------------------------

3. Installation Instructions

Prerequisites
    Python 3.10+
    Poetry (https://python-poetry.org)

Steps
Step 1 — Clone the Repository
    git clone https://github.com/yourusername/literature-review-assistant
    cd literature-review-assistant

Step 2 — Install dependencies with Poetry
    poetry install

Step 3 - Activate the virtual environment (optional, can use poetry run command instead)
    poetry shell 

--------------------------------------------------------------------

4. Usage

Step 1 - Start the MCP tool server (FastMCP)
    Open a terminal, activate the Poetry env, then:
    cd backend
    poetry run python mcp_server.py

Step 2 - Start the Flask controller
    Open another terminal (or use same environment), then:
    cd backend
    poetry run python controller.py

    This runs the Flask app at http://0.0.0.0:3000/.

Step 3 - Open the Frontend
    Open a browser and visit: http://0.0.0.0:3000/