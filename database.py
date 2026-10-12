import sqlite3


def create_database():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        email TEXT,
        phone TEXT,
        education TEXT,
        college TEXT,
        experience TEXT,
        skills TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_candidate(
    name,
    email,
    phone,
    education,
    college,
    experience,
    skills
):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates
    (
        name,
        email,
        phone,
        education,
        college,
        experience,
        skills
    )
    VALUES
    (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        email,
        phone,
        education,
        college,
        experience,
        skills
    ))

    conn.commit()
    conn.close()

def get_all_candidates():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_candidate_count():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM candidates")

    count = cursor.fetchone()[0]

    conn.close()

    return count

def search_candidates(skill):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM candidates
        WHERE skills LIKE ?
        """,
        ('%' + skill + '%',)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def calculate_match(candidate_skills, required_skills):

    candidate_set = set(
        skill.strip().lower()
        for skill in candidate_skills.split(',')
    )

    required_set = set(
        skill.strip().lower()
        for skill in required_skills
    )

    matched = candidate_set.intersection(required_set)

    score = (
        len(matched) / len(required_set)
    ) * 100

    return round(score, 2)

def calculate_ats_score(
    candidate_skills,
    candidate_education,
    candidate_experience,
    required_skills,
    required_education,
    required_experience
):

    skill_score = 0
    education_score = 0
    experience_score = 0

    candidate_skill_set = set(
        skill.strip().lower()
        for skill in candidate_skills.split(',')
    )

    required_skill_set = set(
        skill.strip().lower()
        for skill in required_skills
    )

    matched_skills = candidate_skill_set.intersection(
        required_skill_set
    )

    if len(required_skill_set) > 0:

        skill_score = (
            len(matched_skills)
            / len(required_skill_set)
        ) * 60

    if required_education.lower() in candidate_education.lower():

        education_score = 20

    if required_experience.lower() in candidate_experience.lower():

        experience_score = 20

    final_score = (
        skill_score
        + education_score
        + experience_score
    )

    return {

        'skill_score': round(skill_score, 2),

        'education_score': education_score,

        'experience_score': experience_score,

        'final_score': round(final_score, 2)

    }

def get_candidate_by_id(candidate_id):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates WHERE id=?",
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    return candidate