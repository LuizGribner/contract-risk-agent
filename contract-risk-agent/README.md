AI Contract Risk Analysis Agent

A lightweight system for analyzing contract documents using both rule-based logic and LLM-powered contextual analysis (Gemini API).
This project was built specifically for the Contracts Connected technical challenge.

⸻

1. What the system does

The application can:
	•	Upload and read PDF or TXT files
	•	Extract text automatically
	•	Detect whether the document is or is not a contract
	•	If not a contract, classify the document type and explain why
	•	If it is a contract, analyze risks using:
	•	A deterministic rule engine
	•	An AI-powered Gemini model
	•	Return structured results (title, explanation, severity, remediation, snippet)

⸻

2. Tech Stack

Backend
	•	FastAPI
	•	Python 3
	•	pdfplumber + PyPDF2
	•	Pydantic
	•	Gemini API (google-genai)

Frontend
	•	HTML + CSS
	•	Vanilla JavaScript
	•	Direct file upload to the backend

⸻

3. AI Integration (Gemini)

The system uses a Gemini model (gemini-2.0-flash-lite) to:
	•	Determine if the uploaded file is a contract
	•	Explain why it is or is not
	•	Generate AI-powered risks when applicable
	•	Combine AI findings with deterministic rules

Fallback logic ensures the system continues functioning even if API quota is exceeded.

⸻

4. Project Structure

contract-risk-agent/
├── backend/
│   ├── main.py               # FastAPI app, LLM + rule-engine orchestration
│   ├── analyzer.py           # Deterministic rule-based risk analysis
│   ├── extractor.py          # PDF/TXT extraction
│   ├── ai_analyzer.py        # Gemini integration (classification + risk analysis)
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    └── index.html            # Simple UI for uploads + results

5. How to Run

Local (no Docker)
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --reload

Then open:
frontend/index.html

Docker
cd backend
docker build -t contract-agent .
docker run -p 8000:8000 contract-agent

6. Example Output

Non-contract:
{
  "is_contract": false,
  "document_type": "Technical Documentation",
  "reason": "The document describes architecture and implementation rather than legal terms."
}

Contract with risks:
{
  "is_contract": true,
  "risks": [
    {
      "title": "Unlimited liability",
      "explanation": "...",
      "severity": "high",
      "remediation": "Add a liability cap...",
      "clause_snippet": "..."
    }
  ]
}