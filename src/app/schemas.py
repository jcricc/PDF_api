from pydantic import BaseModel, Field
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str = Field(..., example="Discuss the impact of global warming on polar bears.", description="The essay prompt from which to generate content.")
    author_name: Optional[str] = Field(None, description="Author's name for MLA formatting.")
    instructor_name: Optional[str] = Field(None, description="Instructor's name for MLA formatting.")
    course_name: Optional[str] = Field(None, description="Course name for MLA formatting.")
    date: Optional[str] = Field(None, description="Date for MLA formatting.")

class PDFResponse(BaseModel):
    message: str = Field(..., example="PDF generated successfully.")
    pdf_url: Optional[str] = Field(None, description="URL to the generated PDF document.")
