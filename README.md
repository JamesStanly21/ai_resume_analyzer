# AI Resume Analyzer (Version 1)

A clean, beginner-friendly web application built with **FastAPI** and **Vanilla JavaScript** that analyzes a candidate's resume (PDF) against a target job description.

---

## 📁 Project Structure

```text
Hackathon/
│
├── main.py              # FastAPI backend application & API endpoints
├── analyzer.py          # PDF text extraction and rule-based skill analyzer
├── requirements.txt     # Python dependencies
├── README.md            # Setup and execution guide
│
└── static/              # Frontend web files
    ├── index.html       # HTML UI (upload form & results card)
    ├── style.css        # Clean, modern CSS styling
    └── script.js        # Vanilla JS handling file upload & API calls
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3, FastAPI, Uvicorn, PyPDF
- **Frontend**: HTML5, CSS3, JavaScript (no build tools or heavy frameworks required)

---

## 🚀 How to Run the Project (Step-by-Step)

### 1. Open Terminal or PowerShell
Navigate to the project root directory:
```bash
cd "d:\My CourseWeb\Hackathon"
```

### 2. (Optional but Recommended) Activate Virtual Environment
If you are using a virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

### 3. Install Dependencies
Install all required libraries specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Start the Application
Run the backend server using Uvicorn:
```bash
python main.py
```
*Alternatively, you can run:*
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Open in Your Browser
Once the server is running, open your web browser and visit:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

You can also explore FastAPI's interactive Swagger API documentation at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🔍 How Version 1 Analysis Works

1. **PDF Text Extraction**: Extracts raw text from the uploaded PDF document using `pypdf`.
2. **Skill Matching**: Scans both the resume and the job description for common technical and professional skills (e.g., Python, SQL, React, Docker, Machine Learning, Agile).
3. **Scoring**: Computes a percentage match score based on how many skills required by the job are present in the resume.
4. **Recommendations**: Generates actionable suggestions (e.g., missing skills to highlight, resume length guidance).

> **Future Note**: In upcoming versions, the placeholder logic in `analyzer.py` can be seamlessly replaced with an LLM prompt (e.g., Google Gemini API or OpenAI API) without altering the frontend or API contract!
