"""
Summarization using Hugging Face transformers.
Provides `summarize_texts(texts)` that returns list of summaries.
"""
from transformers import pipeline
import os
from dotenv import load_dotenv
load_dotenv()


SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "sshleifer/distilbart-cnn-12-6")


# instantiate lazily
_summarizer = None


def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model=SUMMARIZER_MODEL, device=0 if os.getenv("CUDA_VISIBLE_DEVICES") else -1)
    return _summarizer




def summarize_text(text, max_length=150, min_length=30):
    summarizer = _get_summarizer()
    # guard length
    try:
        out = summarizer(text, max_length=max_length, min_length=min_length, truncation=True)
        return out[0]["summary_text"].strip()
    except Exception as e:
        return f"[Error in summarization: {e}]"
        


def summarize_documents(docs):
    # docs: list of dicts with 'title' and 'abstract'
    results = []
    for d in docs:
        text = d.get("abstract") or ""
        if not text:
            results.append({**d, "summary": ""})
            continue
        s = summarize_text(text)
        results.append({**d, "summary": s})
    return results