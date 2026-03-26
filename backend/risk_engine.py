# risk engine - assigns levels based on what was found

RISK_WEIGHTS = {
    'password': 10,
    'api_key': 7,
    'phone': 4,
    'email': 2,
    'error': 3
}

def get_risk_level(score):
    if score >= 15:
        return 'CRITICAL'
    elif score >= 8:
        return 'HIGH'
    elif score >= 4:
        return 'MEDIUM'
    else:
        return 'LOW'

def calculate_risk(findings):
    total_score = 0

    for item in findings:
        ftype = item.get('type', '')
        # add weight based on finding type
        total_score += RISK_WEIGHTS.get(ftype, 1)

    level = get_risk_level(total_score)
    return total_score, level
