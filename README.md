AI Contract Risk Analysis Agent

This project is a lightweight AI assisted system that analyzes contract documents and highlights potential legal and commercial risks. It was built specifically for the “AI Contract Risk Analysis Agent” technical test.

1. What the system does
- Upload PDF or TXT files
- Extract text automatically
- Run a rule based risk detection engine
- Identify missing clauses, vague terms, and legal exposure
- Output risks with title, explanation, severity, optional excerpt, and recommended remediation

2. Tech stack
Backend: FastAPI, Python, pdfplumber, Pydantic
Frontend: HTML, CSS, Vanilla JavaScript
Containerization: Docker

3. Main features
- Single endpoint: POST /analyze
- Automatic PDF and text extraction
- Keyword based rule engine
- High, medium and low severity scoring
- Clause snippet extraction
- Optional remediation suggestions

4. Project structure
backend/
  main.py
  analyzer.py
  extractor.py
  requirements.txt
  Dockerfile
frontend/
  index.html
assets/
  sample files (optional)

5. Running locally
cd contract-risk-agent/backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload

Open frontend/index.html in the browser.

6. Running with Docker
cd backend
docker build -t contract-agent .
docker run -p 8000:8000 contract-agent

Swagger is available at:
http://localhost:8000/docs

7. Improvements possible
- LLM based clause analysis
- Advanced rule sets
- DOCX and OCR support
- Export to PDF or HTML
- Saved reports and authentication

8. Why it satisfies the test
- Reads and analyzes contract documents
- Identifies multiple types of risks
- Provides clear explanations and recommendations
- Simple UI for upload and viewing results
- Clean and modular backend structure
- Fully runnable locally or via Docker