from flask import Blueprint, request, jsonify
from services.groq_client import call_groq_with_retry, sanitise_input
from datetime import datetime, timezone
import json
import os

generate_report_bp = Blueprint('generate_report', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Day 6 — POST /generate-report
@generate_report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()

    if not data or not data.get('input_text'):
        return jsonify({"error": "input_text is required"}), 400

    # Day 3 — sanitise input
    try:
        input_text = sanitise_input(data['input_text'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    prompt_path = os.path.join(BASE_DIR, 'prompts', 'generate_report_prompt.txt')
    prompt_template = open(prompt_path).read()
    prompt = prompt_template.replace("{input_text}", input_text) \
                            .replace("{generated_at}", datetime.now(timezone.utc).isoformat())

    try:
        raw = call_groq_with_retry(prompt)
        result = json.loads(raw)
    except Exception:
        # Day 9 — fallback template on Groq error
        return jsonify({
            "is_fallback": True,
            "title": "Report Unavailable",
            "summary": "Could not generate report at this time.",
            "overview": "",
            "key_items": [],
            "recommendations": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }), 200

    return jsonify(result), 200
