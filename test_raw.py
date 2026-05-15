import sys, re, json
sys.path.insert(0, '.')
from app.config import config
from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=config.gemini_api_key)
prompt = '''Return ONLY valid JSON:
{
  "score": 6.0,
  "mistakes": ["example mistake"],
  "correct_answer": "example answer",
  "suggestions": ["example suggestion"]
}'''

response = client.models.generate_content(
    model=config.gemini_model,
    contents=prompt,
    config=genai_types.GenerateContentConfig(temperature=0.2, max_output_tokens=512)
)
raw = response.text
print("=== RAW START ===")
print(repr(raw[:500]))
print("=== RAW END ===")

# Try the fix
cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
cleaned = re.sub(r"\s*```\s*$", "", cleaned, flags=re.MULTILINE)
print("\n=== CLEANED ===")
print(repr(cleaned[:300]))

json_match = re.search(r"\{[\s\S]*\}", cleaned)
if json_match:
    print("\n=== MATCHED JSON ===")
    print(repr(json_match.group()[:200]))
    data = json.loads(json_match.group())
    print("PARSED OK:", data)
else:
    print("NO MATCH FOUND")
