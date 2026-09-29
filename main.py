from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from analyzer import extract_text_from_pdf, analyze_resume

app = FastAPI(
    title="AI Resume Analyzer",
    description="A simple, beginner-friendly API to analyze resumes against job descriptions."
)

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount the static directory to serve CSS, JS, and images
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def get_index():
    """
    Serves the main frontend page.
    """
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AI Resume Analyzer Backend is running. Place index.html in the static folder."}


@app.post("/api/analyze")
async def analyze_endpoint(
    resume: UploadFile = File(..., description="PDF file of the candidate resume"),
    job_description: str = Form(..., description="Target job description text")
):
    """
    Receives a PDF resume and a target job description, extracts text,
    and returns match score, skills found, missing skills, and recommendations.
    """
    # 1. Validate file format
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a PDF file."
        )

    # 2. Validate job description input
    cleaned_job_desc = job_description.strip()
    if not cleaned_job_desc:
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty. Please paste the job requirements."
        )

    # 3. Read uploaded PDF bytes
    try:
        pdf_bytes = await resume.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read uploaded file: {str(e)}"
        )

    if len(pdf_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF file is empty. Please upload a valid document."
        )

    # 4. Extract text from PDF
    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF. Please check if your PDF is scanned or image-only."
        )

    # 5. Run analysis logic
    analysis_result = analyze_resume(resume_text, cleaned_job_desc)

    return analysis_result


if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000 with auto-reload enabled
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
