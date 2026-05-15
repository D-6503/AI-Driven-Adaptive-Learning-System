import sys, os
sys.path.insert(0, '.')
from app.config import config
from app.services.vector_store import get_vector_store
from app.services.embeddings import embed_query
from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=config.gemini_api_key)

store = get_vector_store(1)
qvec = embed_query("State Newton's first law of motion.")
results = store.search(qvec, top_k=5)
context = "\n\n---\n\n".join([r['text'] for r in results])

prompt = f"""You are a strict NCERT Physics examiner evaluating a Class 11 student's answer.

QUESTION: State Newton's first law of motion.

STUDENT'S ANSWER: An object at rest stays at rest unless acted upon by an external force.

REFERENCE CONTEXT (from NCERT Physics textbook):
{context[:5000]}

EVALUATION CRITERIA (total 10 points):
1. Conceptual Accuracy (0–4 pts): Are the physics concepts correctly understood and applied?
2. Completeness (0–3 pts): Has the student covered all key points?
3. Terminology & Units (0–3 pts): Are correct physics terms, formulas, and SI units used?

STRICT RULES:
- Base your evaluation ONLY on the reference context and standard physics principles
- Do NOT give full marks if key concepts are missing
- Mistakes must be specific (not vague)
- The correct answer must be concise but complete
- Suggestions should be actionable and educational

Return ONLY valid JSON — no markdown, no extra text:
{{
  "score": 7.5,
  "mistakes": [
    "Missing mention of Newton's second law (F = ma)",
    "Did not include SI units for velocity"
  ],
  "correct_answer": "Complete model answer here based on the context...",
  "suggestions": [
    "Review Newton's laws of motion in Chapter 5",
    "Always include SI units in your answers"
  ]
}}"""

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=genai_types.GenerateContentConfig(temperature=0.2)
    )
    print('Finish Reason:', response.candidates[0].finish_reason)
    print('Raw Output:')
    print(response.text)
except Exception as e:
    print('Error:', e)
