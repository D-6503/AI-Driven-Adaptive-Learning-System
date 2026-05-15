import sys, re, json
sys.path.insert(0, '.')
from app.config import config
from app.services.vector_store import get_vector_store
from app.services.embeddings import embed_query
from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=config.gemini_api_key)

# Get context
store = get_vector_store(1)
qvec = embed_query("Newton's first law of motion")
results = store.search(qvec, top_k=3)
context = "\n\n---\n\n".join([r["text"] for r in results])

# Build eval prompt (simplified)
prompt = f"""You are a strict NCERT Physics examiner.

QUESTION: State Newton's first law of motion.
STUDENT'S ANSWER: An object at rest stays at rest unless acted upon by an external force.
REFERENCE CONTEXT: {context[:1000]}

Return ONLY valid JSON:
{{
  "score": 7.5,
  "mistakes": ["example"],
  "correct_answer": "Full answer here",
  "suggestions": ["suggestion"]
}}"""

response = client.models.generate_content(
    model=config.gemini_model,
    contents=prompt,
    config=genai_types.GenerateContentConfig(temperature=0.2, max_output_tokens=2048)
)
raw_original = response.text
print("=== ORIGINAL RAW repr (all) ===")
print(repr(raw_original))
print()
