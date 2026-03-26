import re

# patterns to detect sensitive stuff in logs
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'\b(\+?\d{1,3}[\s-]?)?(\d{10}|\d{3}[\s-]\d{3}[\s-]\d{4})\b'
API_KEY_PATTERN = r'(api[_-]?key|apikey|token)\s*[=:]\s*["\']?([A-Za-z0-9_\-]{16,})["\']?'
PASSWORD_PATTERN = r'(password|passwd|pwd)\s*[=:]\s*\S+'

def find_sensitive_data(lines):
    findings = []

    for i, line in enumerate(lines):
        line_num = i + 1

        # check for email addresses
        emails = re.findall(EMAIL_PATTERN, line)
        for e in emails:
            findings.append({
                'type': 'email',
                'line': line_num,
                'match': e,
                'context': line.strip()
            })

        # check for phone numbers
        phones = re.findall(PHONE_PATTERN, line)
        for p in phones:
            num = ''.join(p)
            if len(num) >= 10:
                findings.append({
                    'type': 'phone',
                    'line': line_num,
                    'match': num,
                    'context': line.strip()
                })

        # check for api keys
        api_matches = re.findall(API_KEY_PATTERN, line, re.IGNORECASE)
        for m in api_matches:
            findings.append({
                'type': 'api_key',
                'line': line_num,
                'match': m[1][:8] + '****',  # hide part of the key
                'context': line.strip()
            })

        # check password in log
        if re.search(PASSWORD_PATTERN, line, re.IGNORECASE):
            match = re.search(PASSWORD_PATTERN, line, re.IGNORECASE)
            findings.append({
                'type': 'password',
                'line': line_num,
                'match': '***hidden***',
                'context': line.strip()
            })

        # check for error/exception lines
        if 'error' in line.lower() or 'exception' in line.lower() or 'traceback' in line.lower():
            findings.append({
                'type': 'error',
                'line': line_num,
                'match': line.strip()[:60],
                'context': line.strip()
            })

    return findings
