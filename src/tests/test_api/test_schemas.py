from app.schemas import PromptRequest, PDFResponse
from pydantic import ValidationError
import pytest

def test_prompt_request_schema():
    # Test valid data
    data = {
        "prompt": "Test Prompt",
        "author_name": "John Doe",
        "instructor_name": "Jane Smith",
        "course_name": "English 101",
        "date": "2023-05-01",
    }
    prompt_request = PromptRequest(**data)
    assert prompt_request.prompt == "Test Prompt"
    assert prompt_request.author_name == "John Doe"
    assert prompt_request.instructor_name == "Jane Smith"
    assert prompt_request.course_name == "English 101"
    assert prompt_request.date == "2023-05-01"

    # Test missing required field
    with pytest.raises(ValidationError):
        PromptRequest(prompt="Test Prompt")
        PromptRequest()

def test_pdf_response_schema():
    # Test valid data
    data = {
        "message": "PDF generated successfully",
        "pdf_url": "https://example.com/pdf/test.pdf",
    }
    pdf_response = PDFResponse(**data)
    assert pdf_response.message == "PDF generated successfully"
    assert pdf_response.pdf_url == "https://example.com/pdf/test.pdf"

    # Test missing required field
    with pytest.raises(ValidationError):
        PDFResponse()
