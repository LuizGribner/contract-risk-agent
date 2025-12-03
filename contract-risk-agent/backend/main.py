from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from extractor import extract_text_from_file
from analyzer import analyze_contract_text
from ai_analyzer import analyze_with_llm


class Risk(BaseModel):
    title: str
    explanation: str
    severity: str
    remediation: Optional[str] = None
    clause_snippet: Optional[str] = None


class AnalysisResult(BaseModel):
    is_contract: bool
    risks: Optional[List[Risk]] = None
    document_type: Optional[str] = None
    reason: Optional[str] = None


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
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    text = extract_text_from_file(content, file.content_type)

    llm = analyze_with_llm(text)

    # NÃO É CONTRATO
    if llm.get("is_contract") is False:
        return AnalysisResult(
            is_contract=False,
            document_type=llm.get("document_type", "unknown"),
            reason=llm.get("reason", "Not provided")
        )

    # É CONTRATO → combinar regras + IA
    rule_risks = analyze_contract_text(text)
    llm_risks_raw = llm.get("risks", [])

    llm_risks = [
        Risk(
            title=item.get("title", "Untitled"),
            explanation=item.get("explanation", ""),
            severity=item.get("severity", "low"),
            remediation=item.get("remediation")
        )
        for item in llm_risks_raw
    ]

    combined = rule_risks + llm_risks

    return AnalysisResult(
        is_contract=True,
        risks=combined
    )