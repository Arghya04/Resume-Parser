import csv
from flask import Flask, render_template, request, Response
import os
from database import save_candidate, get_all_candidates, get_candidate_count, search_candidates, calculate_match, calculate_ats_score, get_candidate_by_id

from parser.resume_parser import (
    extract_text,
    extract_email,
    extract_phone,
    extract_skills,
    extract_name,
    extract_education,
    extract_college,
    extract_experience,
    calculate_resume_score,
)

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():

    total_resumes = get_candidate_count()

    return render_template(
        'index.html',
        total_resumes=total_resumes
    )


@app.route('/upload', methods=['POST'])
def upload_resume():

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text(filepath)

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    college = extract_college(resume_text)
    experience = extract_experience(resume_text)
    resume_score, strengths, suggestions = calculate_resume_score(
    name,
    email,
    phone,
    education,
    college,
    skills,
    experience
    )
    if resume_score >= 90:
        grade = "A+"
    elif resume_score >= 80:
        grade = "A"
    elif resume_score >= 70:
        grade = "B"
    elif resume_score >= 60:
        grade = "C"
    else:
        grade = "D"

    save_candidate(
    name,
    email,
    phone,
    education,
    college,
    ", ".join(experience),
    ", ".join(skills)
    )

    return render_template(
    'results.html',
    name=name,
    email=email,
    phone=phone,
    skills=skills,
    education=education,
    college=college,
    experience=experience,
    resume_score=resume_score,
    strengths=strengths,
    suggestions=suggestions,
    )

@app.route('/candidates')
def candidates():

    all_candidates = get_all_candidates()

    return render_template(
        'candidates.html',
        candidates=all_candidates
    )

@app.route('/export')
def export_data():

    candidates = get_all_candidates()

    def generate():

        yield 'ID,Name,Email,Phone,Education,College,Experience,Skills\n'

        for candidate in candidates:

            yield (
                f'{candidate[0]},'
                f'{candidate[1]},'
                f'{candidate[2]},'
                f'{candidate[3]},'
                f'{candidate[4]},'
                f'{candidate[5]},'
                f'"{candidate[6]}",'
                f'"{candidate[7]}"\n'
            )

    return Response(
        generate(),
        mimetype='text/csv',
        headers={
            'Content-Disposition':
            'attachment; filename=candidates.csv'
        }
    )

@app.route('/search')
def search():

    skill = request.args.get('skill')

    results = []

    if skill:

        results = search_candidates(skill)

    return render_template(
        'search.html',
        results=results
    )

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():

    ranked_candidates = []

    if request.method == 'POST':

        required_skills = request.form[
            'required_skills'
        ].split(',')

        required_education = request.form[
            'required_education'
        ]

        required_experience = request.form[
            'required_experience'
        ]

        candidates = get_all_candidates()

        for candidate in candidates:

            scores = calculate_ats_score(
                candidate[7],   # skills
                candidate[4],   # education
                candidate[6],   # experience
                required_skills,
                required_education,
                required_experience
            )

            ranked_candidates.append({

                'name': candidate[1],

                'skills_score':
                scores['skill_score'],

                'education_score':
                scores['education_score'],

                'experience_score':
                scores['experience_score'],

                'final_score':
                scores['final_score']

            })

        ranked_candidates.sort(
            key=lambda x: x['final_score'],
            reverse=True
        )

    return render_template(
    'ranking.html',
    ranked_candidates=ranked_candidates,
    required_skills=', '.join(required_skills) if request.method == 'POST' else '',
    required_education=required_education if request.method == 'POST' else '',
    required_experience=required_experience if request.method == 'POST' else ''
    )

@app.route('/candidate/<int:id>')
def candidate_profile(id):

    candidate = get_candidate_by_id(id)

    if not candidate:
        return "Candidate not found"

    return render_template(
        "profile.html",
        candidate=candidate
    )

if __name__ == '__main__':
    app.run(debug=True)