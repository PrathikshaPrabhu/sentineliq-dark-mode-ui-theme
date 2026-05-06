from flask import Blueprint, request, jsonify
from services.groq_client import call_groq_with_retry
from datetime import datetime, timezone
import json, os

describe_bp = Blueprint('describe', __name__)

def load_prompt(filename):
    path = os.path.join('prompts', filename)
    with open(path, 'r') as f:
        return f.read()

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('details'):
        return jsonify({"error": "name and details are required"}), 400

    prompt = load_prompt('describe_prompt.txt').format(
        name=data['name'],
        details=data['details'],
        generated_at=datetime.now(timezone.utc).isoformat()
    )

    try:
        raw = call_groq_with_retry(prompt)
        result = json.loads(raw)
    except Exception as e:
        return jsonify({"is_fallback": True, "description": "Could not generate at this time."}), 200

    return jsonify(result), 200