import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def safe_json_loads(text):
    """
    Remove qualquer coisa antes/depois do JSON e tenta carregar.
    """
    text = text.strip()

    # Tenta carregar direto
    try:
        return json.loads(text)
    except:
        pass

    # Para casos em que a IA inclui texto extra
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        cleaned = text[start:end]
        return json.loads(cleaned)
    except:
        return None


def analyze_with_llm(text):
    prompt = f"""
You are an AI specialized in document classification and contract risk analysis.

Step 1:
Determine if the text is a CONTRACT or NOT a contract.

If NOT a contract:
Identify the document type (e.g., email, report, project note, technical documentation, invoice, schedule).
Explain clearly WHY it is not a contract.

If YES (it IS a contract):
Extract contract risk items.
Each item must contain:
- "title"
- "explanation"
- "severity" (high, medium, low)
- "remediation"

OUTPUT FORMAT (strict JSON only):

If NOT a contract:
{{
  "is_contract": false,
  "document_type": "...",
  "reason": "..."
}}

If a contract:
{{
  "is_contract": true,
  "risks": [
    {{
      "title": "...",
      "explanation": "...",
      "severity": "high/medium/low",
      "remediation": "..."
    }}
  ]
}}

Return ONLY JSON. No explanations. No markdown.
Document text:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text
    except Exception as e:
        print("LLM error:", e)
        return {
            "is_contract": False,
            "document_type": "unknown",
            "reason": str(e)
        }

    data = safe_json_loads(raw)
    if data is None:
        print("LLM error: invalid JSON returned")
        return {
            "is_contract": False,
            "document_type": "unknown",
            "reason": "LLM output unreadable"
        }

    return data