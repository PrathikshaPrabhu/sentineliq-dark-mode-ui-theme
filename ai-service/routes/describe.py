from flask import Blueprint, request, jsonify
from services.groq_client import call_groq_with_retry, sanitise_input
from datetime import datetime, timezone
import json
import os

describe_bp = Blueprint('describe', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_prompt(filename):
    path = os.path.join(BASE_DIR, 'prompts', filename)
    with open(path, 'r') as f:
        return f.read()


# Day 3 — POST /describe
@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('details'):
        return jsonify({"error": "name and details are required"}), 400

    # Day 3 — sanitise inputs
    try:
        name = sanitise_input(data['name'])
        details = sanitise_input(data['details'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt = load_prompt('describe_prompt.txt').format(
        name=name,
        details=details,
        generated_at=datetime.now(timezone.utc).isoformat()
    )

    try:
        raw = call_groq_with_retry(prompt)
        result = json.loads(raw)
    except Exception:
        # Day 9 — fallback template on Groq error
        return jsonify({
            "is_fallback": True,
            "description": "Could not generate at this time.",
            "tags": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }), 200

    return jsonify(result), 200
