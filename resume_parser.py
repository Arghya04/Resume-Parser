import pdfplumber
from docx import Document
import re


SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "machine learning",
    "data science",
    "sql",
    "html",
    "css",
    "flask",
    "django",
    "javascript",
    "react",
    "tailwind",
    "mongodb",
    "mysql",
    "opencv",
    "deep learning",
    "ai",
    "artificial intelligence"
]
DEGREE_DB = [
    "b.tech",
    "btech",
    "b.e",
    "be",
    "b.sc",
    "bsc",
    "m.tech",
    "mtech",
    "m.sc",
    "msc",
    "bca",
    "mca",
    "mba",
    "phd"
]
EXPERIENCE_KEYWORDS = [
    "intern",
    "internship",
    "engineer",
    "developer",
    "analyst",
    "consultant",
    "manager",
    "executive",
    "specialist"
]


def extract_text(file_path):

    text = ""

    if file_path.endswith('.pdf'):

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    elif file_path.endswith('.docx'):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


def extract_email(text):

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    email = re.findall(email_pattern, text)

    return email[0] if email else "Not Found"


def extract_phone(text):

    phone_pattern = r'\+?\d[\d -]{8,13}\d'

    phone = re.findall(phone_pattern, text)

    return phone[0] if phone else "Not Found"


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS_DB:

        if skill in text:
            found_skills.append(skill.title())

    return found_skills


def extract_name(text):

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    invalid_words = {
        "intern", "internship", "developer", "engineer", "analyst",
        "manager", "marketing", "tester", "current", "experience",
        "skills", "education", "contact", "summary", "profile",
        "linkedin", "github", "email", "phone", "objective",
        "projects", "certifications", "address", "mobile",
        "career", "technical", "manual", "csr", "work"
    }

    # -------- First Preference: Full name on one line --------
    for line in lines[:10]:

        words = line.split()

        if 2 <= len(words) <= 4:

            if all(word.replace(".", "").isalpha() for word in words):

                if not any(word.lower() in invalid_words for word in words):

                    return line

    # -------- Second Preference: Name split into two lines --------
    for i in range(min(10, len(lines)-1)):

        first = lines[i]
        second = lines[i+1]

        if len(first) <= 2:      # Ignore initials like SK
            continue

        if not first.isalpha():
            continue

        if not second.isalpha():
            continue

        if first.lower() in invalid_words:
            continue

        if second.lower() in invalid_words:
            continue

        return first + " " + second

    return "Not Found"

def extract_education(text):

    text_lower = text.lower()

    for degree in DEGREE_DB:

        if degree in text_lower:
            return degree.upper()

    return "Not Found"

def extract_college(text):

    lines = text.split('\n')

    college_keywords = [
        "university",
        "college",
        "institute",
        "iit",
        "nit",
        "iiit",
        "iem",
        "makaut",
        "academy",
        "school of engineering"
    ]

    for line in lines:

        cleaned = line.strip()

        lower = cleaned.lower()

        if any(keyword in lower for keyword in college_keywords):

            # Remove GPA information
            if "gpa" in lower:
                cleaned = cleaned.split("GPA")[0]

            # Remove "Education:" if present
            cleaned = re.sub(
                r'Education\s*:\s*',
                '',
                cleaned,
                flags=re.IGNORECASE
            )

            return cleaned.strip()

    return "Not Found"

def extract_experience(text):

    lines = text.split('\n')

    experiences = []

    for line in lines:

        cleaned = line.strip()

        if len(cleaned) > 60:
            continue

        keywords = [
            "intern",
            "engineer",
            "developer",
            "analyst",
            "specialist",
            "consultant",
            "manager"
        ]

        for keyword in keywords:

            if keyword in cleaned.lower():

                if cleaned not in experiences:
                    experiences.append(cleaned)

    return experiences

def calculate_resume_score(
    name,
    email,
    phone,
    education,
    college,
    skills,
    experience
):

    score = 0
    strengths = []
    suggestions = []

    # Name
    if name != "Not Found":
        score += 10
        strengths.append("Name detected")
    else:
        suggestions.append("Add your full name clearly at the top")

    # Email
    if email != "Not Found":
        score += 10
        strengths.append("Professional email found")
    else:
        suggestions.append("Include a professional email address")

    # Phone
    if phone != "Not Found":
        score += 10
        strengths.append("Contact number available")
    else:
        suggestions.append("Include your phone number")

    # Education
    if education != "Not Found":
        score += 15
        strengths.append("Education section detected")
    else:
        suggestions.append("Add your education details")

    # College
    if college != "Not Found":
        score += 10
        strengths.append("College information found")
    else:
        suggestions.append("Mention your college or university")

    # Skills
    if len(skills) >= 8:
        score += 25
        strengths.append("Excellent technical skill set")

    elif len(skills) >= 5:
        score += 20
        strengths.append("Good technical skills")

    elif len(skills) >= 3:
        score += 15
        strengths.append("Basic technical skills")

    else:
        suggestions.append("Include more technical skills")

    # Experience
    if len(experience) > 0:
        score += 20
        strengths.append("Experience section available")
    else:
        suggestions.append("Add internships, projects or work experience")

    return score, strengths, suggestions