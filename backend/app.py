from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import run_analysis

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend

@app.route('/')
def home():
    return "Log Analyzer API is running!"

# main endpoint - accepts log content and returns analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'No content provided'}), 400

    log_text = data['content']

    if len(log_text.strip()) == 0:
        return jsonify({'error': 'Content is empty'}), 400

    result = run_analysis(log_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
