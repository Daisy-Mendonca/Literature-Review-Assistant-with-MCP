from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from src.orchestration import run_pipeline
from fastapi.templating import Jinja2Templates


app = FastAPI(title="AI Literature Review Assistant")


# mount static
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


class ReviewRequest(BaseModel):
    query: str
    sources: list[str] = ["arxiv"]
    max_papers: int = 5


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/review", response_class=HTMLResponse)
async def review_post(request: Request, query: str = Form(...), sources: str = Form("arxiv"), max_papers: int = Form(5)):
    # sources comes as comma-separated from form
    sources_list = [s.strip() for s in sources.split(",") if s.strip()]
    review = await run_pipeline(query=query, sources=sources_list, max_papers=max_papers)
    # save markdown
    out_dir = "data/outputs"
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, f"review_{query[:40].replace(' ','_')}.md")
    with open(md_path, "w", encoding="utf-8") as f:
    f.write(review["markdown"])
    return templates.TemplateResponse("results.html", {"request": request, "review": review})


@app.get("/download")
async def download(path: str):
    # path should be a server-side path under data/outputs
    return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))