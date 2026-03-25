from log_parser import parse_log
from utils import find_sensitive_data
from risk_engine import calculate_risk

# generate simple text insights from findings
def generate_insights(findings):
    messages = []
    types_found = [f['type'] for f in findings]

    if 'password' in types_found:
        messages.append("Sensitive credentials found in logs - remove immediately.")

    if 'api_key' in types_found:
        messages.append("API key exposed in log file - rotate the key.")

    if 'email' in types_found:
        count = types_found.count('email')
        messages.append(f"{count} email address(es) found - check privacy compliance.")

    if 'phone' in types_found:
        messages.append("Phone number detected - potential privacy issue.")

    error_count = types_found.count('error')
    if error_count >= 2:
        messages.append(f"{error_count} errors/exceptions detected - system may be unstable.")
    elif error_count == 1:
        messages.append("One error detected in logs.")

    if len(messages) == 0:
        messages.append("No major issues found in this log.")

    return messages


# main function - takes raw log text and returns full report
def run_analysis(log_text):
    lines = parse_log(log_text)
    findings = find_sensitive_data(lines)
    score, level = calculate_risk(findings)
    insights = generate_insights(findings)

    summary = {
        'total_lines': len(lines),
        'total_findings': len(findings),
    }

    return {
        'summary': summary,
        'findings': findings,
        'risk_score': score,
        'risk_level': level,
        'insights': insights
    }
