# this file reads log data and splits it into lines

def parse_log(log_text):
    # split by newline and remove blank lines
    lines = log_text.split('\n')
    cleaned = []
    for line in lines:
        if line.strip() != '':
            cleaned.append(line)
    return cleaned
