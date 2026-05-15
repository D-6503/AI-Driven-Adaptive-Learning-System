# OptiLearn AI 🧠

> A RAG-Based Intelligent System for Automated Question Generation, Answer Evaluation, and Learning Analytics

**OptiLearn AI** uses a complete end-to-end AI pipeline to transform NCERT Physics PDFs into an interactive learning experience:
- Upload PDFs → extract & chunk text → embed with `sentence-transformers`
- Store in **FAISS** vector database for semantic retrieval
- Generate **Bloom's Taxonomy** questions (Remembering / Understanding / Application) via **Gemini 1.5 Flash**
- Evaluate student answers with **RAG-powered** Gemini prompts → score + feedback
- Track learning performance with **Recharts** analytics dashboard

---

## 🗂️ Project Structure

```
optilearn-ai/
├── backend/           # Flask API + RAG pipeline
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/    # ORM + Pydantic schemas
│   │   ├── services/  # PDF, FAISS, Gemini, Analytics
│   │   └── routes/    # Flask blueprints
│   ├── data/          # SQLite + FAISS index + uploads
│   ├── main.py
│   └── requirements.txt
│
└── frontend/          # React + TypeScript + Vite
    ├── src/
    │   ├── components/ # Upload, Quiz, Analytics
    │   ├── pages/      # Home, Quiz, Results, Dashboard
    │   ├── services/   # Axios API client
    │   └── types/      # TypeScript interfaces
    └── package.json
```

---

## ⚙️ Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

---

## 🚀 Quick Start

### 1. Clone & Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
```

Edit `.env` and add your **Gemini API key**:
```env
GEMINI_API_KEY=your_actual_key_here
```

Get a free key at → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 3. Start the Backend

```bash
python main.py
```

✅ Backend running at `http://localhost:5000`

### 4. Set Up Frontend

```bash
cd ../frontend
npm install
npm run dev
```

✅ Frontend running at `http://localhost:5173`

---

## 🎮 How to Use

1. **Open** `http://localhost:5173`
2. **Upload** an NCERT Physics chapter PDF (drag & drop)
3. Wait for ✅ "Successfully Processed!" — chunks are embedded in FAISS
4. Click **Start Quiz** on your document
5. Enter your name and configure question mix (Remembering / Understanding / Application)
6. Click **Generate Questions & Start** — Gemini creates questions
7. Answer each question and submit
8. See your **Score + Mistakes + Model Answer + Suggestions**
9. Visit **Dashboard** to see your chapter accuracy, trends, and weak topics

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | System health check |
| `POST` | `/api/documents/upload` | Upload & process PDF |
| `GET` | `/api/documents/` | List all documents |
| `DELETE` | `/api/documents/<id>` | Delete document |
| `POST` | `/api/questions/generate` | Generate questions (Gemini) |
| `GET` | `/api/questions/<doc_id>` | List questions for document |
| `POST` | `/api/questions/session` | Create quiz session |
| `POST` | `/api/questions/session/<id>/complete` | Complete session |
| `POST` | `/api/evaluate/` | Evaluate student answer (RAG + Gemini) |
| `GET` | `/api/evaluate/session/<id>` | Get session responses |
| `GET` | `/api/analytics/<user_id>` | Get learning analytics |

---

## 🧠 RAG Pipeline

```
PDF Upload
    │
    ▼
PyMuPDF (text extraction) → Chapter Detection
    │
    ▼
Semantic Chunking (~500 tokens, 50 overlap)
    │
    ▼
sentence-transformers/all-MiniLM-L6-v2 (embeddings)
    │
    ▼
FAISS IndexFlatIP (per-document index)
    │
    ▼ (at query time)
Question: embed query → FAISS top-5 → Context
    │
    ▼
Gemini 1.5 Flash (question generation / answer evaluation)
    │
    ▼
SQLite (persist sessions, responses, analytics)
```

---

## 📊 Supported NCERT Chapters

1. Motion in a Straight Line (Kinematics)
2. Motion in a Plane (Vectors, Projectile)
3. Laws of Motion (Newton's Laws, Friction)
4. Work, Energy and Power
5. Rotational Motion
6. Gravitation
7. Mechanical Properties of Solids
8. Mechanical Properties of Fluids

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.x |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS (faiss-cpu) |
| Structured DB | SQLite + SQLAlchemy |
| PDF | PyMuPDF (fitz) |
| Frontend | React 18 + TypeScript + Vite |
| Charts | Recharts |
| Styling | Vanilla CSS (glassmorphism design) |
| HTTP | Axios |
| Notifications | react-hot-toast |
| Icons | Lucide React |

---

## 🔑 Environment Variables

```env
GEMINI_API_KEY=           # Required — Google AI Studio key
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=               # Random secret for Flask sessions
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=data/uploads
FAISS_INDEX_DIR=data/faiss_index
SQLITE_DB_PATH=data/optilearn.db
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `GEMINI_API_KEY not set` | Add key to `backend/.env` |
| `faiss-cpu` install fails | Try `pip install faiss-cpu --no-cache-dir` |
| `sentence-transformers` slow first run | Model downloads on first use (~90MB) |
| CORS errors | Ensure frontend runs on port 5173 and backend on 5000 |
| PDF extraction returns empty | Ensure PDF is text-based (not scanned image) |

---

## 📝 License

MIT License — Free for educational use.
