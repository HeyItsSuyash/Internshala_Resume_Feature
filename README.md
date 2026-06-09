# Internshala Resume Intelligence MVP

This project transforms the existing Internshala prototype into a fully functional MVP with a Python/FastAPI backend, robust PDF/DOCX parsing, and an intelligent role-matching engine powered by Groq.

## Features Added
- **Resume Vault:** Securely store up to 5 parsed resumes in an SQLite database.
- **Groq Parsing:** Extracts `Name`, `Education`, `Skills`, `Experience`, `Projects`, and `Certifications` directly into a structured JSON payload via the LLaMA3 model.
- **Smart Resume Recommendation:** Evaluates stored resumes against job descriptions to suggest the best fit.
- **Application Flow:** Displays Strengths, Weaknesses, and Missing Skills inside the pre-apply modal before persisting applications to the database.

## Local Setup

1. **Prerequisites:** Python 3.10+
2. **Environment Variable:** Set your Groq API Key.
   ```bash
   $env:GROQ_API_KEY="gsk_your_api_key_here"
   ```
3. **Install Dependencies:**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Run Server:**
   ```bash
   uvicorn main:app --reload
   ```
   *Note: The frontend is statically served at `http://localhost:8000/search_internships.html`*

## Deployment to Render

This project is configured to deploy instantly on Render using the included `render.yaml`.

1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New > Blueprint**.
3. Connect your repository containing this code.
4. Render will automatically detect the `render.yaml` configuration.
5. Provide the `GROQ_API_KEY` when prompted in the Render environment variables UI.
6. Deploy! The Web Service will host both the FastAPI backend and serve the static HTML frontend.
