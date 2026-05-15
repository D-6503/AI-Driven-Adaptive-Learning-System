# -*- coding: utf-8 -*-
"""
OptiLearn AI — Comprehensive Backend Test Suite
Tests every API endpoint systematically.
"""
import sys
import io
import requests
import json
import os
import time

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "http://localhost:5000/api"
PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"

results = {"pass": 0, "fail": 0, "skip": 0}

def test(name, condition, detail=""):
    if condition is None:
        print(f"  {SKIP} {name}" + (f" — {detail}" if detail else ""))
        results["skip"] += 1
    elif condition:
        print(f"  {PASS} {name}")
        results["pass"] += 1
    else:
        print(f"  {FAIL} {name}" + (f" — {detail}" if detail else ""))
        results["fail"] += 1

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ──────────────────────────────────────────────────────────────
section("1. HEALTH CHECK")
# ──────────────────────────────────────────────────────────────
try:
    r = requests.get(f"{BASE}/health", timeout=5)
    test("GET /api/health returns 200", r.status_code == 200)
    test("Health response has status=ok", r.json().get("status") == "ok")
    test("Health response has app name", "OptiLearn" in r.json().get("app", ""))
except Exception as e:
    test("Backend reachable", False, str(e))

# ──────────────────────────────────────────────────────────────
section("2. DOCUMENTS API")
# ──────────────────────────────────────────────────────────────
doc_id = None
try:
    r = requests.get(f"{BASE}/documents/", timeout=5)
    test("GET /api/documents/ returns 200", r.status_code == 200)
    data = r.json()
    test("Response has 'documents' key", "documents" in data)
    test("Response has 'total' key", "total" in data)
    docs = data.get("documents", [])
    test("At least one document exists", len(docs) > 0, f"Found {len(docs)} docs")
    if docs:
        doc_id = docs[0]["id"]
        ready_doc = next((d for d in docs if d["status"] == "ready"), None)
        if ready_doc:
            doc_id = ready_doc["id"]
        test("First document has required fields", all(k in docs[0] for k in ["id","chapter","status","chunk_count"]))
        test("A document has status=ready", ready_doc is not None, f"doc_id={doc_id}")
except Exception as e:
    test("Documents API reachable", False, str(e))

# Test single document fetch
if doc_id:
    try:
        r = requests.get(f"{BASE}/documents/{doc_id}", timeout=5)
        test(f"GET /api/documents/{doc_id} returns 200", r.status_code == 200)
        test("Document detail has chapter field", "chapter" in r.json())
    except Exception as e:
        test("Single document fetch", False, str(e))

# ──────────────────────────────────────────────────────────────
section("3. QUESTION GENERATION & MCQ")
# ──────────────────────────────────────────────────────────────
generated_questions = []
if doc_id:
    try:
        payload = {"document_id": doc_id, "n_remembering": 2, "n_understanding": 1, "n_application": 1}
        print(f"  ⏳ Generating questions for doc_id={doc_id} (may take ~15s)...")
        r = requests.post(f"{BASE}/questions/generate", json=payload, timeout=90)
        test("POST /api/questions/generate returns 201", r.status_code == 201, f"Got {r.status_code}: {r.text[:100]}")
        if r.status_code == 201:
            data = r.json()
            generated_questions = data.get("questions", [])
            test("Questions returned", len(generated_questions) > 0, f"Got {len(generated_questions)}")
            test("Total questions count is correct", data.get("total") == len(generated_questions))

            # Test MCQ structure
            if generated_questions:
                q = generated_questions[0]
                test("Question has 'text' field", bool(q.get("text")))
                test("Question has 'question_type' field", q.get("question_type") in ["remembering","understanding","application"])
                test("Question has 'difficulty' field", q.get("difficulty") in ["easy","medium","hard"])
                test("Question has MCQ 'options' field", isinstance(q.get("options"), dict), f"options={q.get('options')}")
                test("MCQ has 4 options (A-D)", len(q.get("options", {})) == 4, f"Got {len(q.get('options', {}))}")
                test("Question has 'correct_option' field", q.get("correct_option") in ["A","B","C","D"], f"Got: {q.get('correct_option')}")
    except Exception as e:
        test("Question generation", False, str(e))
else:
    test("Question generation", None, "Skipped — no doc_id available")

# ──────────────────────────────────────────────────────────────
section("4. QUIZ SESSION CREATION")
# ──────────────────────────────────────────────────────────────
session_id = None
if generated_questions and doc_id:
    try:
        q_ids = [q["id"] for q in generated_questions]
        payload = {
            "user_id": "test_user_001",
            "user_name": "Test Student",
            "document_id": doc_id,
            "question_ids": q_ids
        }
        r = requests.post(f"{BASE}/questions/session", json=payload, timeout=10)
        test("POST /api/questions/session returns 201", r.status_code == 201, f"Got {r.status_code}")
        if r.status_code == 201:
            data = r.json()
            session_id = data.get("session_id")
            test("Session ID returned", session_id is not None)
            test("Session has user_name", data.get("user_name") == "Test Student")
            test("Session total_questions correct", data.get("total_questions") == len(q_ids))
    except Exception as e:
        test("Session creation", False, str(e))
else:
    test("Session creation", None, "Skipped — no questions generated")

# ──────────────────────────────────────────────────────────────
section("5. ANSWER EVALUATION")
# ──────────────────────────────────────────────────────────────
if session_id and generated_questions:
    try:
        q = generated_questions[0]
        # For MCQ, build an answer from a selected option
        selected = q.get("correct_option", "A")
        answer_text = f"{selected}: {q.get('options', {}).get(selected, 'Test Answer')}"
        
        payload = {
            "session_id": session_id,
            "question_id": q["id"],
            "student_answer": answer_text,
        }
        print(f"  ⏳ Evaluating answer (may take ~10s)...")
        r = requests.post(f"{BASE}/evaluate/", json=payload, timeout=90)
        test("POST /api/evaluate/ returns 201", r.status_code == 201, f"Got {r.status_code}: {r.text[:150]}")
        if r.status_code == 201:
            data = r.json()
            ev = data.get("evaluation", {})
            test("Evaluation has 'score' field", "score" in ev)
            test("Score is between 0 and 10", 0 <= ev.get("score", -1) <= 10, f"Score: {ev.get('score')}")
            test("Evaluation has 'correct_answer'", bool(ev.get("correct_answer")))
            test("Evaluation has 'mistakes' list", isinstance(ev.get("mistakes"), list))
            test("Evaluation has 'suggestions' list", isinstance(ev.get("suggestions"), list))
    except Exception as e:
        test("Answer evaluation", False, str(e))
else:
    test("Answer evaluation", None, "Skipped — no session/questions")

# ──────────────────────────────────────────────────────────────
section("6. SESSION COMPLETION & RESULTS")
# ──────────────────────────────────────────────────────────────
if session_id:
    try:
        # Complete session
        r = requests.post(f"{BASE}/questions/session/{session_id}/complete", timeout=10)
        test("POST /api/questions/session/complete returns 200", r.status_code == 200)
        
        # Fetch session results
        r = requests.get(f"{BASE}/evaluate/session/{session_id}", timeout=10)
        test("GET /api/evaluate/session/<id> returns 200", r.status_code == 200)
        if r.status_code == 200:
            data = r.json()
            test("Session result has 'responses'", "responses" in data)
            test("Session result has 'avg_score'", "avg_score" in data)
            test("Session result has 'user_name'", data.get("user_name") == "Test Student")
    except Exception as e:
        test("Session completion", False, str(e))
else:
    test("Session completion", None, "Skipped — no session_id")

# ──────────────────────────────────────────────────────────────
section("7. YOUTUBE RECOMMENDATIONS")
# ──────────────────────────────────────────────────────────────
try:
    chapters_to_test = ["Mechanical Properties of Fluids", "Laws of Motion", "Unknown Chapter XYZ"]
    for chapter in chapters_to_test:
        r = requests.get(f"{BASE}/recommendations/{requests.utils.quote(chapter)}", timeout=5)
        test(f"GET /api/recommendations/{chapter[:25]}... returns 200", r.status_code == 200)
        if r.status_code == 200:
            data = r.json()
            test(f"  → Has 'videos' list", isinstance(data.get("videos"), list))
            test(f"  → Returns at least 1 video", len(data.get("videos", [])) >= 1, f"Got {len(data.get('videos',[]))}")
            if data.get("videos"):
                v = data["videos"][0]
                test(f"  → Video has title/url/thumbnail", all(k in v for k in ["title","url","thumbnail"]))
except Exception as e:
    test("Recommendations API", False, str(e))

# ──────────────────────────────────────────────────────────────
section("8. ANALYTICS API")
# ──────────────────────────────────────────────────────────────
try:
    r = requests.get(f"{BASE}/analytics/test_user_001", timeout=5)
    test("GET /api/analytics/<user_id> returns 200", r.status_code == 200)
    if r.status_code == 200:
        data = r.json()
        test("Analytics has 'chapter_accuracy'", "chapter_accuracy" in data)
        test("Analytics has 'session_trends'", "session_trends" in data)
        test("Analytics has 'overall_avg_score'", "overall_avg_score" in data)
except Exception as e:
    test("Analytics API", False, str(e))

# ──────────────────────────────────────────────────────────────
section("9. ERROR HANDLING")
# ──────────────────────────────────────────────────────────────
try:
    r = requests.get(f"{BASE}/documents/999999", timeout=5)
    test("Non-existent document returns 404", r.status_code == 404)
    
    r = requests.get(f"{BASE}/evaluate/session/999999", timeout=5)
    test("Non-existent session returns 404", r.status_code == 404)
    
    r = requests.post(f"{BASE}/evaluate/", json={}, timeout=5)
    test("Empty evaluate body returns 400", r.status_code == 400)
    
    r = requests.post(f"{BASE}/questions/generate", json={}, timeout=5)
    test("Empty generate body returns 400", r.status_code == 400)
except Exception as e:
    test("Error handling", False, str(e))

# ──────────────────────────────────────────────────────────────
section("FINAL RESULTS")
# ──────────────────────────────────────────────────────────────
total = results["pass"] + results["fail"] + results["skip"]
print(f"\n  Total:   {total}")
print(f"  ✅ Pass:  {results['pass']}")
print(f"  ❌ Fail:  {results['fail']}")
print(f"  ⚠️  Skip:  {results['skip']}")
score = int((results['pass'] / max(results['pass'] + results['fail'], 1)) * 100)
print(f"\n  Score:   {score}% ({results['pass']}/{results['pass'] + results['fail']} passing tests)")
print()
