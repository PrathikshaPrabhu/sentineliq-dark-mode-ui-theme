from flask import Flask
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp
import os

load_dotenv()

app = Flask(__name__)

# Day 3 — Rate limiter 30 req/min per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

# Day 8 — Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Register all blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(health_bp)

# Day 11 — Pre-load ChromaDB at startup
with app.app_context():
    try:
        from services.chroma_client import init_chroma
        init_chroma()
        print("[Startup] ChromaDB initialised successfully")
    except Exception as e:
        print(f"[Startup] ChromaDB init skipped: {e}")

@app.route('/')
def index():
    return {
        "status": "AI Service Running",
        "version": "3.0",
        "endpoints": [
            "POST /describe",
            "POST /recommend",
            "POST /generate-report",
            "GET  /health"
        ]
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)