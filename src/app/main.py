from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from weasyprint import HTML
import tempfile
import os
from app.dependencies import verify_token, get_query_validator  # Adjust import paths as necessary
from app.schemas import PromptRequest, PDFResponse  # Adjust import paths as necessary

app = FastAPI()

@app.post("/generate-pdf/", response_model=PDFResponse)
async def generate_pdf(
    request: PromptRequest,
    background_tasks: BackgroundTasks,
    x_token: str = Depends(verify_token),
    q: str = Depends(get_query_validator)  # Corrected get_query_validator usage
):
    # Generate HTML from prompt and query
    html_content = await mock_html(request.prompt, q)

    # Convert HTML to PDF in background task
    pdf_path = await html_to_pdf(html_content, background_tasks)

    # Assuming we store or make the PDF accessible via URL
    # This URL should reflect where and how the PDF is actually stored or served
    pdf_url = f"http://example.com/pdf/{os.path.basename(pdf_path)}"

    return PDFResponse(message="PDF generated successfully.", pdf_url=pdf_url)

async def mock_html(prompt, query):
    # Mock HTML content generation based on prompt and query
    return f"<html><body><h1>{prompt}</h1><p>This is a generated content based on: {prompt}. Query was: {query}</p></body></html>"

async def html_to_pdf(html_content, background_tasks: BackgroundTasks):
    # Convert HTML content to PDF file using WeasyPrint in an asynchronous function call
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    # Using HTML.write_pdf in a synchronous context might block the event loop
    # Consider running it in a thread pool
    HTML(string=html_content).write_pdf(target=temp_file.name)
    background_tasks.add_task(cleanup_file, temp_file.name)
    # Schedule cleanup after response
    return temp_file.name

def cleanup_file(file_path):
    try:
        os.unlink(file_path)
    except OSError as e:
        # Adding logging for file deletion failure
        print(f"Error deleting temporary file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

