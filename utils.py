import re

def mask_pii(text):
    entities = []

    def mask_and_record(pattern, label, mask_tag):
        nonlocal text
        for match in re.finditer(pattern, text):
            entity = match.group()
            start, end = match.start(), match.end()
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": entity
            })
        text = re.sub(pattern, f"[{mask_tag}]", text)
    
    patterns = [
        (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'email', 'email'),
        (r'\b(?:\+91[-\s]?)?[789]\d{9}\b', 'phone_number', 'phone_number'),
        (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', 'credit_debit_no', 'credit_debit_no'),
        (r'\b\d{3}\b', 'cvv_no', 'cvv_no'), 
        (r'\b\d{2}/\d{2}\b', 'expiry_no', 'expiry_no'),
        (r'\b\d{12}\b', 'aadhar_num', 'aadhar_num'),
        (r'\b\d{4}-\d{2}-\d{2}\b', 'dob', 'dob'), 
    ]

    for pattern, label, tag in patterns:
        mask_and_record(pattern, label, tag)

    return text, entities

