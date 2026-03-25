A secure data intelligence platform (SIDP) is an information system designed to help businesses confirm the security of their data and enable business continuity in the event that data is lost or stolen (Buchanan and Huczynski, 2004).

And one of the projects that students made, I created to present to SISA. It is a basic principle, feed it with log files and it will search through them and find useful sensitive information such as passwords, emails, API keys, etc. Then it presents you with some information and some degree of risk.

---

## What it does

- Log files scan API keys, -n passwords, email, phone numbers.
- contains a risk score and a risk level (LOW / MEDiocre / HIGH/ CRITical)
- States exact line where there is a problem.
- It is possible to paste text or to attach a.log file.

---

## Tech used

- Backend: Python + Flask
- Frontend: Plain HTML, CSS, JavaScript (no frameworks)
- Detection: Python regex

---

## How to run it

Step 1 - Clone or download the project

```
git clone https://github.com/yourusername/SIDP.git
cd SIDP
```

Step 2 - Install backend dependencies

```
cd backend
pip install -r requirements.txt
```

Step 3 - Start the Flask server

```
python app.py
```

You should see something like: `Running on http://127.0.0.1:5000`

Step 4 - Open frontend

Just open `frontend/index.html` in your browser. No server needed for the frontend.

---

## Example

Input (paste this in the textarea):

```
2024-03-01 09:13:03 INFO User logged in: john@example.com
2024-03-01 09:14:00 DEBUG password=admin123
2024-03-01 09:15:10 ERROR NullPointerException at line 42
```

Output:
```
Risk Level: CRITICAL
Risk Score: 17
Insights:
  - Sensitive credentials found in logs - remove immediately.
  - 1 email address(es) found - check privacy compliance.
  - One error detected in logs.
```

---

## Project Structure

```
AI-Secure-Data-Intelligence-Platform/
├── backend/
│   ├── app.py         
│   ├── analyzer.py     
│   ├── log_parser.py   
│   ├── risk_engine.py 
│   ├── utils.py        
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── sample_logs/
│   └── test.log        <- sample log to test with
└── README.md
```

---

## Notes

- This is a beginner-level project, not production-ready
- Made for learning purposes as part of a cybersecurity course
- If Flask is not running, the frontend will show a connection error

---

Made by: Nitish Kumar | Submission: SISA Project
