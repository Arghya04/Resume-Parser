# 🤖 AI-Powered Resume Parser & Applicant Tracking System (ATS)

An intelligent web-based Resume Parser and Applicant Tracking System designed to automate resume screening, candidate analysis, and recruitment management.

The system extracts candidate information from PDF/DOCX resumes, evaluates resume quality, ranks candidates using ATS-based matching, and provides personalized resume feedback.

---

## 🚀 Features

- 📄 Upload resumes in PDF and DOCX formats
- 🔍 Automatic resume information extraction
- 👤 Candidate profile management
- 📧 Email and phone number extraction
- 🎓 Education and college extraction
- 🛠️ Technical skill detection
- 💼 Experience extraction
- 📊 Resume Quality Score
- ⭐ Personalized resume strengths and suggestions
- 🏆 ATS-based candidate ranking
- 🔎 Candidate search functionality
- 📋 Detailed Candidate Analysis
- 📤 CSV data export
- 💾 SQLite database storage
- 🎨 Responsive and modern user interface

---

## 🧠 AI & NLP Techniques

The project uses a lightweight rule-based intelligent processing approach rather than a generative AI model.

### Techniques Used

- Rule-Based Natural Language Processing (NLP)
- Regular Expressions (Regex)
- Keyword Matching
- Heuristic Scoring
- ATS Skill Matching
- Resume Information Extraction

These techniques are used to identify relevant candidate information and evaluate resumes according to predefined criteria.

---

## 🛠️ Technology Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- Tailwind CSS
- Jinja2 Templates

### Resume Processing
- pdfplumber
- python-docx
- Regular Expressions

### Development
- Visual Studio Code
- Git & GitHub

---

## 📂 Project Structure

```text
Resume-Parser-ATS/
│
├── app.py
├── database.py
├── resume_parser.py
├── database.db
│
├── templates/
│   ├── index.html
│   ├── candidates.html
│   ├── ranking.html
│   ├── results.html
│   ├── search.html
│   └── profile.html
│
├── uploads/
│
└── README.md
