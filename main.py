"""
OptiLearn AI — Flask Application Entry Point
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from app.database import init_db
from app.routes.documents import documents_bp
from app.routes.questions import questions_bp
from app.routes.evaluation import evaluation_bp
from app.routes.analytics import analytics_bp
from app.routes.voice import voice_bp
from app.routes.recommendations import recommendations_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Config ─────────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB upload limit

    # ── CORS ───────────────────────────────────────────────────────────────
    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}})

    # ── Blueprints ─────────────────────────────────────────────────────────
    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    app.register_blueprint(questions_bp, url_prefix="/api/questions")
    app.register_blueprint(evaluation_bp, url_prefix="/api/evaluate")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(voice_bp, url_prefix="/api/voice")
    app.register_blueprint(recommendations_bp, url_prefix="/api/recommendations")

    # ── Health check ───────────────────────────────────────────────────────
    @app.route("/api/health")
    def health():
        return {"status": "ok", "app": "OptiLearn AI", "version": "1.0.0"}

    return app


if __name__ == "__main__":
    # Ensure data directories exist
    for path in ["data/uploads", "data/faiss_index"]:
        os.makedirs(path, exist_ok=True)

    # Initialise SQLite tables
    init_db()

    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    print(f"\n[*] OptiLearn AI backend running on http://localhost:{port}")
    print("[*] Ready to process NCERT Physics PDFs!\n")
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")
