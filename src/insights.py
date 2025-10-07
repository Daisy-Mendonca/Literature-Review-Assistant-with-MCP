"""
Lightweight synthesis: combines summaries and uses a HF generation model to produce
key insights, trends, and suggested research gaps.
"""
from transformers import pipeline
import os
from dotenv import load_dotenv
load_dotenv()
SYNTHESIS_MODEL = os.getenv("SYNTHESIS_MODEL", "bigscience/bloomz-1b1")


_generator = None


def _get_generator():
    global _generator
    if _generator is None:
        _generator = pipeline("text-generation", model=SYNTHESIS_MODEL, device=0 if os.getenv("CUDA_VISIBLE_DEVICES") else -1)
    return _generator


PROMPT_TEMPLATE = """
You are an academic assistant. Given the following paper summaries, produce:
1) A 3-sentence high-level synthesis.
2) 5 bullet point key insights/trends.
3) 3 suggested research gaps/opportunities.


Summaries:
{summaries}


Respond with markdown: 'SYNTHESIS', 'INSIGHTS', 'GAPS' sections.
"""




def generate_insights(summaries: list[str]):
    generator = _get_generator()
    joined = "\n\n".join([f"- {s}" for s in summaries])
    prompt = PROMPT_TEMPLATE.format(summaries=joined)
    out = generator(prompt, max_length=512, do_sample=False)
    text = out[0]["generated_text"]
    return text