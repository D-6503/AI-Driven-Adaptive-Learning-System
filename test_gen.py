import sys
sys.path.insert(0, '.')
from app.services.question_generator import generate_questions

try:
    result = generate_questions(
        document_id=1,
        chapter='Motion in a Straight Line',
        n_remembering=2,
        n_understanding=1,
        n_application=1
    )
    print("SUCCESS:", len(result), "questions generated")
    for q in result:
        diff = q["difficulty"]
        qtype = q["question_type"]
        text = q["text"][:80]
        print(f"  [{diff}] ({qtype}) {text}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print("ERROR:", e)
