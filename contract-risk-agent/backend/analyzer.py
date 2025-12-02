import re

def analyze_contract_text(text):
    text_lower = text.lower()
    risks = []

    def add(title, explanation, severity, term, remediation=None):
        risks.append({
            "title": title,
            "explanation": explanation,
            "severity": severity,
            "clause_snippet": extract_snippet(text, term) if term else None,
            "remediation": remediation
        })

    if not any(x in text_lower for x in ["insurance", "liability insurance"]):
        add(
            "Insurance not mentioned",
            "The contract does not include any requirement for insurance coverage.",
            "high",
            "insurance",
            "Add a clause requiring the counterparty to maintain adequate liability and commercial insurance."
        )

    if "unlimited liability" in text_lower:
        add(
            "Unlimited liability",
            "The contract suggests unlimited liability exposure.",
            "high",
            "liability",
            "Introduce a liability cap appropriate to the value and risks of the agreement."
        )

    if not any(x in text_lower for x in ["payment", "fee", "compensation"]):
        add(
            "Vague payment terms",
            "No clear terms regarding deadlines or payment conditions.",
            "medium",
            "payment",
            "Specify payment deadlines, amounts, method of invoicing, and late-payment penalties."
        )

    if any(x in text_lower for x in ["broad indemnification", "full indemnification"]):
        add(
            "Overly broad indemnification",
            "The contract includes wide indemnification obligations.",
            "high",
            "indemnification",
            "Narrow the indemnification clause to exclude indirect damages and limit obligations to direct harm."
        )

    if not any(x in text_lower for x in ["terminate", "termination", "end the agreement"]):
        add(
            "Missing termination clause",
            "The contract does not specify how the parties may terminate the agreement.",
            "medium",
            "termination",
            "Add a termination for convenience and termination for cause clause with notice periods."
        )

    if not any(x in text_lower for x in ["confidential", "non-disclosure", "nda"]):
        add(
            "No confidentiality clause",
            "The agreement does not reference confidentiality obligations.",
            "medium",
            "confidential",
            "Include confidentiality or NDA language to protect proprietary information."
        )

    if not any(x in text_lower for x in ["intellectual property", "ip ownership"]):
        add(
            "IP ownership unclear",
            "The contract does not specify IP ownership.",
            "medium",
            "intellectual property",
            "Define whether IP is owned by the provider, the client, or jointly, and include license rights."
        )

    if not any(x in text_lower for x in ["liability cap", "limited liability"]):
        add(
            "Liability cap missing",
            "The contract does not establish a maximum liability amount.",
            "high",
            "liability",
            "Introduce a liability cap proportional to contract value, typically 1x contract fees."
        )

    if not any(x in text_lower for x in ["dispute", "arbitration", "jurisdiction"]):
        add(
            "Missing dispute resolution clause",
            "No method for resolving disputes is provided.",
            "low",
            "dispute",
            "Add a dispute resolution clause specifying mediation, arbitration, or court jurisdiction."
        )

    if not any(x in text_lower for x in ["governing law", "laws of"]):
        add(
            "Missing governing law",
            "The contract does not specify applicable jurisdiction.",
            "low",
            "law",
            "Define the governing law and venue to avoid legal ambiguity."
        )

    if any(x in text_lower for x in ["auto-renew", "automatic renewal"]):
        add(
            "Automatic renewal clause",
            "The contract may renew automatically without explicit approval.",
            "medium",
            "renew",
            "Add a requirement for written renewal confirmation before the renewal takes effect."
        )

    if any(x in text_lower for x in ["as needed", "as required", "sole discretion"]):
        add(
            "Ambiguous obligations",
            "The agreement contains vague or discretionary obligations.",
            "medium",
            "discretion",
            "Clarify performance obligations with measurable and objective criteria."
        )

    return risks


def extract_snippet(text, term):
    pattern = r".{0,80}" + re.escape(term) + r".{0,80}"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(0) if match else None