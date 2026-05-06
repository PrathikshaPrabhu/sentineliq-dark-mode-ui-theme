from flask import Blueprint, request, jsonify
from services.groq_client import call_groq_with_retry
import json, os

recommend_bp = Blueprint('recommend', __name__)

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    if not data or not data.get('input_text'):
        return jsonify({"error": "input_text is required"}), 400

    prompt_path = os.path.join(BASE_DIR, 'prompts', 'recommend_prompt.txt')
    prompt_template = open(prompt_path).read()
    prompt = prompt_template.replace("{input_text}", data['input_text'])

    try:
        raw = call_groq_with_retry(prompt)
        result = json.loads(raw)
    except Exception as e:
        return jsonify({"is_fallback": True, "recommendations": []}), 200

    return jsonify(result), 200