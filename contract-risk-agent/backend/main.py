from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from extractor import extract_text_from_file
from analyzer import analyze_contract_text

class Risk(BaseModel):
    title: str
    explanation: str
    severity: str
    clause_snippet: Optional[str] = None
    remediation: Optional[str] = None
class AnalysisResult(BaseModel):
    risks: List[Risk]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="File type not supported")
    content = await file.read()
    text = extract_text_from_file(content, file.content_type)
    risks = analyze_contract_text(text)
    return AnalysisResult(risks=risks)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)