import PyPDF2
from .nlp_service import NLPService

class EmailProcessor:
    def __init__(self):
        self.nlp_service = NLPService()

    def read_email_from_file(self, file_path, file_type):
        if file_type == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_type == '.pdf':
            return self._read_pdf(file_path)
        else:
            raise ValueError("Tipo de arquivo não suportado")

    def _read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

    def process_email(self, email_content):
        processed_text = self.nlp_service.preprocess_text(email_content)
        category, confidence = self.nlp_service.classify_email_productivity(processed_text)
        suggested_response = self.nlp_service.generate_response(category)
        return {
            'category': category,
            'confidence': confidence,
            'suggested_response': suggested_response,
            'processed_text': processed_text
        }