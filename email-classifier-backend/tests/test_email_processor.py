from src.services.email_processor import EmailProcessor

def test_read_email_content():
    processor = EmailProcessor()
    content = processor.read_email_content("path/to/sample_email.txt")
    assert content is not None
    assert isinstance(content, str)

def test_process_email_content():
    processor = EmailProcessor()
    content = "This is a sample email content for testing."
    processed_content = processor.process_email_content(content)
    assert processed_content is not None
    assert isinstance(processed_content, str)
    assert len(processed_content) < len(content)  # Assuming processing reduces content length

def test_invalid_file_path():
    processor = EmailProcessor()
    content = processor.read_email_content("invalid/path/to/email.txt")
    assert content is None  # Expecting None for invalid path