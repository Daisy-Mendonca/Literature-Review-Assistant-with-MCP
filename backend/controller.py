# controller.py
import asyncio
import json
import re
from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from fastmcp.client import Client

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# --------------------
# LLM setup
# --------------------
MODEL = "meta-llama/Meta-Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

PROMPT = """
You are a tool selector. Return JSON only.
These are the tools that you can use:
- search_papers
- get_paper_details

The tool you select should be placed in "action", and the arguments to that tool in "args".
Your response should be in the following JSON format:
{{ "action": "...", "args": {{ ... }} }}

User query: "{query}"
"""

def parse_json_from_model_output(text):
    try:
        # Remove code fences
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except:
        return None

# --------------------
# MCP helper
# --------------------
async def call_mcp_tool(tool_name, args):
    client = Client("http://localhost:8000/sse")  # or SSETransport("http://localhost:8000/sse")
    async with client:
        result = await client.call_tool(tool_name, args)
        return result.data

# --------------------
# Main query handler
# --------------------
@app.post("/query")
def handle_query():
    payload = request.json
    if not payload or "query" not in payload:
        return jsonify({"error": "missing 'query' in json body"}), 400

    user_query = payload["query"]
    prompt = PROMPT.format(query=user_query)

    gen = generator(prompt, max_length=256, do_sample=False)
    model_text = gen[0]["generated_text"]
    print(f"Model output: {model_text}")
    parsed = parse_json_from_model_output(model_text)
    if parsed is None:
        return jsonify({"error": "could not parse model output", "model_output": model_text}), 500

    action = parsed.get("action")
    args = parsed.get("args", {})
    print(f"Action: {action}, Args: {args}")
    try:
        # Call MCP tool
        result = asyncio.run(call_mcp_tool(action, args))
        return jsonify({"action": action, "args": args, "result": result})
    except Exception as e:
        return jsonify({"error": str(e), "trace": repr(e)}), 500

# --------------------
# Serve frontend
# --------------------
@app.get("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.get("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
