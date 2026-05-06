from flask import Flask
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)

@app.route('/')
def index():
    return {"status": "AI Service Running"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)