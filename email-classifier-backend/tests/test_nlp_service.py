import pytest
from src.services.nlp_service import NLPService

@pytest.fixture
def nlp_service():
    return NLPService()

def test_remove_stop_words(nlp_service):
    text = "This is a sample text with some stop words."
    expected_result = "sample text stop words."
    result = nlp_service.remove_stop_words(text)
    assert result == expected_result

def test_stemming(nlp_service):
    text = "running runner ran"
    expected_result = "run run run"
    result = nlp_service.stem_text(text)
    assert result == expected_result

def test_lemmatization(nlp_service):
    text = "better best"
    expected_result = "good good"
    result = nlp_service.lemmatize_text(text)
    assert result == expected_result

def test_preprocess_text(nlp_service):
    text = "This is a sample text for testing."
    expected_result = "sample text testing."
    result = nlp_service.preprocess_text(text)
    assert result == expected_result