from fastmcp import FastMCP
import asyncio
import tools as tools

app = FastMCP(name="Literature Review Assistant", version="0.1.0")

@app.tool
def get_users() -> list[dict]:
    return tools.get_users()

@app.tool
def add_user(first_name:str, last_name:str, email:str) -> dict:
    return tools.add_user(first_name, last_name, email)

@app.tool
def search_papers(query:str, limit:int=5) -> list[dict]:
    return tools.search_papers(query, limit)

@app.tool
def get_paper_details(paper_id:str) -> dict:
    return tools.get_paper_details(paper_id)

@app.tool
def add_reference(title: str, authors: list, year: int, url: str) -> dict:
    return tools.add_reference(title, authors, year, url)

@app.tool
def get_references() -> list[dict]:
    return tools.get_references()


if __name__ == "__main__":
    asyncio.run(app.run_sse_async(host="0.0.0.0", port=8000, log_level="debug"))