from fastapi.testclient import TestClient
from app.main import app  # Adjust according to your project structure
client = TestClient(app)

def test_generate_pdf_success():
    response = client.post(
        "generate-pdf/",
        json={"prompt": "Test Prompt"},  # Adjusted to match PromptRequest schema
        headers={"x-token": "expected_token"}
    )
    assert response.status_code == 200
    assert "PDF generated successfully" in response.json()["message"]
    assert response.json()["pdf_url"]

    response = client.post(
        "/generate-pdf/",
        json={"prompt": "Test Prompt"},
        headers={"x-token": "invalid_token"}
    )
    assert response.status_code == 401
    # Ensure your application logic correctly handles and returns this error.
