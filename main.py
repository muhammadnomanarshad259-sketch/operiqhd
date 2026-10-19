from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import fitz
import re
from datetime import datetime

app = FastAPI(title="OperiqHD", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
decisions = []

class DecisionInput(BaseModel):
    decision: str
    reason: str
    reviewer: str = "Proposal Manager"

def extract_info(text):
    info = {
        "contract_number": "Nahi mila",
        "deadline": "Nahi mila",
        "naics": "Nahi mila",
        "agency": "Nahi mila",
        "company": "Nahi mila"
    }
    match = re.search(r'FFFA-\d+-[A-Z]-\d+', text)
    if match:
        info["contract_number"] = match.group()
    match = re.search(r'October\s+\d+,\s+\d{4}.*?(?:PM|AM)\s+ET', text)
    if match:
        info["deadline"] = match.group()
    match = re.search(r'NAICS\s+(\d{6})', text)
    if match:
        info["naics"] = match.group(1)
    if "federal" in text.lower():
        info["agency"] = "Federal Agency"
    match = re.search(r'Summit\s+Federal\s+Solutions', text)
    if match:
        info["company"] = match.group()
    return info

def analyze_gaps(text):
    gaps = []
    if "Federal Facilities Safety Certification" in text:
        gaps.append({
            "title": "Federal Facilities Safety Certification",
            "detail": "Safety plan hai lekin federal certification nahi hai.",
            "severity": "critical",
            "owner": "Proposal Manager"
        })
    if "2026-12-31" in text or "December 31" in text:
        gaps.append({
            "title": "Insurance Coverage Expiry",
            "detail": "Insurance Dec 31 2026 expire. Contract Jan 1 2027 se shuru.",
            "severity": "high",
            "owner": "Operations Manager"
        })
    if "SFS-011" in text:
        gaps.append({
            "title": "Past Performance POC Missing",
            "detail": "SFS-011 mein POC name phone aur email missing hain.",
            "severity": "high",
            "owner": "Proposal Manager"
        })
    if "Warehouse Specialist" in text:
        gaps.append({
            "title": "Warehouse Specialist Rate Missing",
            "detail": "SFS-014 mein Warehouse Specialist rate nahi hai.",
            "severity": "high",
            "owner": "Pricing Lead"
        })
    if "Amendment" in text:
        gaps.append({
            "title": "Amendment 0001 Acknowledgment",
            "detail": "Amendment 0001 acknowledgment record hona chahiye.",
            "severity": "medium",
            "owner": "Proposal Manager"
        })
    return gaps

@app.get("/")
def home():
    return {"message": "OperiqHD server chal raha hai!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    info = extract_info(text)
    gaps = analyze_gaps(text)
    return {
        "status": "success",
        "filename": file.filename,
        "message": f"{file.filename} upload ho gaya!",
        "info": info,
        "gaps": gaps
    }

@app.post("/decision")
def save_decision(data: DecisionInput):
    decision = {
        "id": len(decisions) + 1,
        "decision": data.decision,
        "reason": data.reason,
        "reviewer": data.reviewer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    decisions.append(decision)
    return {"status": "success", "decision": decision}

@app.get("/decisions")
def get_decisions():
    return {"decisions": decisions}