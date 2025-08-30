from flask import Blueprint, request, jsonify
from src.services.email_processor import EmailProcessor

api = Blueprint('api', __name__)

@api.route('/process-email', methods=['POST'])
def process_email():
    if 'file' not in request.files and 'text' not in request.form:
        return jsonify({'error': 'No email content provided'}), 400

    email_processor = EmailProcessor()

    if 'file' in request.files:
        file = request.files['file']
        email_content = email_processor.read_email_from_file(file)
    else:
        email_content = request.form['text']

    processed_result = email_processor.process_email_content(email_content)

    return jsonify(processed_result), 200