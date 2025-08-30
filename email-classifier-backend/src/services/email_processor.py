class EmailProcessor:
    def __init__(self, nlp_service):
        self.nlp_service = nlp_service

    def read_email_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()
        return email_content

    def process_email(self, email_content):
        processed_content = self.nlp_service.preprocess_text(email_content)
        return processed_content