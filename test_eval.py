import sys
sys.path.insert(0, '.')
from app.services.answer_evaluator import evaluate_answer
import traceback

try:
    result = evaluate_answer(
        question="State Newton's first law of motion.",
        student_answer="An object at rest stays at rest unless acted upon by an external force.",
        document_id=1,
        chapter="Motion in a Straight Line"
    )
    print("SUCCESS!")
    print(f"  Score: {result['score']}/10")
except Exception as e:
    import app.services.answer_evaluator as ev
    traceback.print_exc()
    print("ERROR:", e)
