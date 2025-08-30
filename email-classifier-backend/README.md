# Email Classifier Backend

This project is an email classifier backend that processes email content using natural language processing (NLP) techniques. It allows users to upload email files, which are then analyzed to classify their content and suggest automated responses.

## Project Structure

```
email-classifier-backend
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── email_processor.py
│   │   └── nlp_service.py
│   ├── models
│   │   ├── __init__.py
│   │   └── classification.py
│   └── utils
│       ├── __init__.py
│       ├── text_preprocessing.py
│       └── file_handler.py
├── tests
│   ├── __init__.py
│   ├── test_email_processor.py
│   └── test_nlp_service.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd email-classifier-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Set up environment variables by copying `.env.example` to `.env` and updating the values as needed.

2. Run the application:
   ```
   python src/main.py
   ```

3. Access the API to upload emails and receive classification results.

## Testing

To run the tests, use the following command:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.