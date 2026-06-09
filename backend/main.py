from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
import shutil
import datetime
import json
from pydantic import BaseModel

from parser import extract_text_from_file, parse_resume_with_groq, analyze_match_with_groq

# DB Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./resumes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ResumeDB(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    extracted_text = Column(Text)
    parsed_keywords = Column(Text) # JSON string of the structured Groq data
    is_primary = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class ApplicationDB(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String)
    job_title = Column(String)
    match_score = Column(Integer)
    resume_used = Column(String)
    status = Column(String, default="Applied")
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for the static frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/resumes/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    extracted_text = extract_text_from_file(file_path)
    parsed_json = parse_resume_with_groq(extracted_text)
    
    # If this is the first resume, make it primary
    existing = db.query(ResumeDB).count()
    is_primary = existing == 0

    new_resume = ResumeDB(
        filename=file.filename,
        filepath=file_path,
        extracted_text=extracted_text,
        parsed_keywords=json.dumps(parsed_json),
        is_primary=is_primary
    )
    
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "keywords": parsed_json, # For backwards compatibility, but it's full JSON
        "is_primary": new_resume.is_primary
    }

@app.get("/api/resumes")
def get_resumes(db: Session = Depends(get_db)):
    resumes = db.query(ResumeDB).all()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "keywords": json.loads(r.parsed_keywords) if r.parsed_keywords else {},
            "is_primary": r.is_primary,
            "uploaded_at": r.uploaded_at
        }
        for r in resumes
    ]

@app.put("/api/resumes/{resume_id}/primary")
def set_primary(resume_id: int, db: Session = Depends(get_db)):
    db.query(ResumeDB).update({ResumeDB.is_primary: False})
    
    target = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    target.is_primary = True
    db.commit()
    return {"status": "success", "primary_id": resume_id}

@app.delete("/api/resumes/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    target = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    db.delete(target)
    db.commit()
    
    if target.is_primary:
        next_resume = db.query(ResumeDB).order_by(ResumeDB.uploaded_at.desc()).first()
        if next_resume:
            next_resume.is_primary = True
            db.commit()
            
    return {"status": "success"}

class MatchRequest(BaseModel):
    resume_id: int
    job_requirements: str

@app.post("/api/match")
def match_resume(req: MatchRequest, db: Session = Depends(get_db)):
    resume = db.query(ResumeDB).filter(ResumeDB.id == req.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    resume_json = json.loads(resume.parsed_keywords) if resume.parsed_keywords else {}
    match_data = analyze_match_with_groq(resume_json, req.job_requirements)
    
    return {
        "resume_id": req.resume_id,
        "score": match_data.get("score", 0),
        "strengths": match_data.get("strengths", []),
        "weaknesses": match_data.get("weaknesses", []),
        "missingSkills": match_data.get("missingSkills", [])
    }

class ApplicationRequest(BaseModel):
    job_id: str
    job_title: str
    match_score: int
    resume_used: str

@app.post("/api/applications")
def save_application(req: ApplicationRequest, db: Session = Depends(get_db)):
    new_app = ApplicationDB(
        job_id=req.job_id,
        job_title=req.job_title,
        match_score=req.match_score,
        resume_used=req.resume_used
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {"status": "success", "id": new_app.id}

@app.get("/api/applications")
def get_applications(db: Session = Depends(get_db)):
    apps = db.query(ApplicationDB).order_by(ApplicationDB.applied_at.desc()).all()
    return [
        {
            "id": a.id,
            "jobId": a.job_id,
            "jobTitle": a.job_title,
            "matchScore": a.match_score,
            "resumeUsed": a.resume_used,
            "status": a.status,
            "appliedAt": a.applied_at
        }
        for a in apps
    ]

# Serve frontend statically so we only need one server (Render Web Service friendly)
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
