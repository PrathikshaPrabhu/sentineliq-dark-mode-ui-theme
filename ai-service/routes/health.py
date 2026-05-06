from flask import Blueprint, jsonify
import time

health_bp = Blueprint('health', __name__)
START_TIME = time.time()
_response_times = []


def record_response_time(ms: float):
    _response_times.append(ms)
    if len(_response_times) > 100:
        _response_times.pop(0)


def get_avg_response_time():
    if not _response_times:
        return 0
    return int(sum(_response_times) / len(_response_times))


# Day 7 — GET /health
@health_bp.route('/health', methods=['GET'])
def health():
    uptime_seconds = int(time.time() - START_TIME)
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time_ms": get_avg_response_time() or 800,
        "uptime_seconds": uptime_seconds,
        "endpoints": {
            "describe": "POST /describe",
            "recommend": "POST /recommend",
            "generate_report": "POST /generate-report"
        }
    }), 200
