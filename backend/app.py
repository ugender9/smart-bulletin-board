from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'API Running!'})

@app.route('/api/notices', methods=['POST'])
def create_notice():
    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')
        
        prompt = f"""Analyze: Title: {title}, Content: {content}
Return ONLY JSON: {{"category": "Academic/Event/Deadline/Opportunity/Other", "importance": "low/medium/high", "tags": ["CSE","ECE","MECH","CIVIL"]}}"""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        analysis = json.loads(response.text)
        
        return jsonify({'success': True, 'analysis': analysis}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notices', methods=['GET'])
def get_notices():
    notices = [
        {'id': '1', 'title': 'CSE Exam Schedule', 'category': 'Academic', 'importance': 'high'},
        {'id': '2', 'title': 'Hackathon Registration', 'category': 'Event', 'importance': 'medium'}
    ]
    return jsonify({'notices': notices})

@app.route('/api/notices/search', methods=['GET'])
def search_notices():
    query = request.args.get('q', '')
    return jsonify({'results': [{'id': '1', 'title': 'CSE Exam Schedule'}]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
