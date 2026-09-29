import io
import re
from typing import Dict, List, Any
from pypdf import PdfReader

# A curated list of common technical and professional skills for rule-based matching.
COMMON_SKILLS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift",
    "html", "css", "react", "angular", "vue", "node.js", "express", "fastapi", "django", "flask",
    "sql", "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "linux",
    "machine learning", "deep learning", "nlp", "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "rest api", "graphql", "microservices", "agile", "scrum", "unit testing", "system design",
    "communication", "teamwork", "leadership", "problem solving", "critical thinking"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts plain text from raw PDF bytes using pypdf.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_pages.append(text)
        return "\n".join(extracted_pages).strip()
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")


def _find_skills(text: str) -> set:
    """
    Helper function to match known skills from text in a case-insensitive manner.
    """
    found = set()
    lowered_text = text.lower()
    
    for skill in COMMON_SKILLS:
        # Use regex word boundaries so 'go' doesn't match 'good' or 'django'
        # For skills with symbols like c++, c#, node.js, escape them
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, lowered_text):
            found.add(skill.title() if len(skill) > 3 else skill.upper())
            
    return found


def analyze_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Analyzes resume text against a target job description.
    This is a clean, rule-based placeholder function that will later be replaced by an LLM.
    
    Returns:
        dict: {
            "match_score": int,
            "skills_found": list[str],
            "missing_skills": list[str],
            "recommendations": list[str]
        }
    """
    if not resume_text.strip():
        return {
            "match_score": 0,
            "skills_found": [],
            "missing_skills": [],
            "recommendations": [
                "Could not detect any text in the PDF. Please ensure your PDF is not a scanned image."
            ]
        }

    # 1. Identify skills in the job description and in the resume
    job_skills = _find_skills(job_description)
    resume_skills = _find_skills(resume_text)

    # 2. Determine matching and missing skills
    if job_skills:
        skills_found = sorted(list(job_skills.intersection(resume_skills)))
        missing_skills = sorted(list(job_skills - resume_skills))
        # Match score based on proportion of job skills found
        match_score = int(round((len(skills_found) / len(job_skills)) * 100))
    else:
        # If the job description didn't contain catalog skills, list resume skills detected
        skills_found = sorted(list(resume_skills))
        missing_skills = []
        # Fallback simple keyword overlap score
        job_words = set(re.findall(r'\b\w{4,}\b', job_description.lower()))
        resume_words = set(re.findall(r'\b\w{4,}\b', resume_text.lower()))
        if job_words:
            overlap = job_words.intersection(resume_words)
            match_score = min(int(round((len(overlap) / len(job_words)) * 100)), 85)
        else:
            match_score = 50

    # Clamp match score between 0 and 100
    match_score = max(0, min(100, match_score))

    # 3. Generate practical recommendations
    recommendations = []

    if missing_skills:
        missing_preview = ", ".join(missing_skills[:4])
        recommendations.append(
            f"Add key missing skills mentioned in the job description: {missing_preview}."
        )

    if match_score < 50:
        recommendations.append(
            "Align your project bullet points more closely with the responsibilities in the job posting."
        )
    elif match_score < 75:
        recommendations.append(
            "Good match! Consider highlighting quantifiable results (e.g., 'improved performance by 20%') for existing skills."
        )
    else:
        recommendations.append(
            "Strong match! Ensure your most relevant experiences are prominently featured at the top of your resume."
        )

    # General best-practice advice
    word_count = len(resume_text.split())
    if word_count < 150:
        recommendations.append(
            "Your resume appears very concise. Consider elaborating on key projects and technical achievements."
        )
    elif word_count > 900:
        recommendations.append(
            "Your resume is quite lengthy. Consider condensing it to 1-2 pages for better readability by recruiters."
        )
    else:
        recommendations.append(
            "Use active action verbs (e.g., 'Architected', 'Implemented', 'Optimized') to begin your experience bullet points."
        )

    return {
        "match_score": match_score,
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }
