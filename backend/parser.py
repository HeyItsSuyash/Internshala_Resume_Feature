import os
import json
from groq import Groq

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

# Initialize Groq Client
# Ensure GROQ_API_KEY is set in your environment variables.
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
GROQ_MODEL = "llama3-8b-8192"

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".pdf" and PdfReader:
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            
    elif ext in [".doc", ".docx"] and Document:
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            
    else:
        # Fallback for txt or unsupported formats
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except:
            pass

    return text

def parse_resume_with_groq(text: str) -> dict:
    """Uses Groq API to parse the raw resume text into structured JSON."""
    if not os.environ.get("GROQ_API_KEY"):
        # Fallback if no API key is provided
        return {
            "name": "Unknown",
            "education": ["Extracted Education"],
            "skills": ["JavaScript", "Python", "Communication"],
            "experience": ["Extracted Experience"],
            "projects": ["Extracted Projects"],
            "certifications": ["Extracted Certifications"]
        }

    prompt = f"""
    You are an expert ATS (Applicant Tracking System) parser.
    Extract the following information from the provided resume text and return it strictly as a JSON object.
    Do NOT include any markdown formatting, explanations, or introductory text. Just the raw JSON.

    Required JSON structure:
    {{
        "name": "string",
        "education": ["string", "string"],
        "skills": ["string", "string"],
        "experience": ["string", "string"],
        "projects": ["string", "string"],
        "certifications": ["string", "string"]
    }}

    Resume Text:
    {text}
    """

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        response_text = completion.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        print(f"Groq API Error in parse_resume: {e}")
        # Return fallback on error
        return {
            "name": "Error Parsing",
            "education": [],
            "skills": [],
            "experience": [],
            "projects": [],
            "certifications": []
        }

def analyze_match_with_groq(resume_json: dict, job_requirements_text: str) -> dict:
    """Uses Groq API to calculate a match score and provide insights."""
    if not os.environ.get("GROQ_API_KEY"):
        # Fallback
        return {
            "score": 75,
            "strengths": ["Basic Requirements Met"],
            "weaknesses": ["Cannot perform deep analysis without API key"],
            "missingSkills": []
        }

    prompt = f"""
    You are an expert HR recruiter and ATS system.
    Analyze the following Resume against the Internship Description.
    Generate a Role Match Score (0 to 100), identify the candidate's strengths for this role, weaknesses, and any explicitly missing skills required by the job description but not found in the resume.
    Return strictly as a JSON object. No markdown, no explanations.

    Required JSON structure:
    {{
        "score": integer,
        "strengths": ["string", "string"],
        "weaknesses": ["string", "string"],
        "missingSkills": ["string", "string"]
    }}

    Resume Data (JSON):
    {json.dumps(resume_json)}

    Internship Description:
    {job_requirements_text}
    """

    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        response_text = completion.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        print(f"Groq API Error in analyze_match: {e}")
        return {
            "score": 50,
            "strengths": ["Error analyzing"],
            "weaknesses": ["Error analyzing"],
            "missingSkills": []
        }
