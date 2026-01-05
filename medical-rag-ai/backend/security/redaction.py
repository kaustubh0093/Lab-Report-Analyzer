import re

def redact_phi(text: str) -> str:
    """
    Redact potential PHI (Personal Health Information) from text using Regex.
    Targeting: SSNs, Phone Numbers, Dates (simple heuristic).
    """
    # SSN (XXX-XX-XXXX)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', text)
    
    # Phone (simple 10 digit or variants)
    text = re.sub(r'\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b', '[REDACTED_PHONE]', text)
    
    # Dates (MM/DD/YYYY or YYYY-MM-DD) - Aggressive redaction might hide test dates, so be careful.
    # For now, let's just redact obvious DOB patterns if labeled
    text = re.sub(r'(?i)DOB:?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', 'DOB: [REDACTED_DATE]', text)
    
    return text
