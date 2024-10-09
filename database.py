import sqlite3
from fuzzywuzzy import fuzz

# Initialize the new single-table database structure with hash column
def initialize_db():
    conn = sqlite3.connect('data/resume_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_hash TEXT,
            skills TEXT,
            work_experience TEXT,
            industries TEXT,
            describe_yourself TEXT,
            question TEXT,
            response_generated TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to get previous questions for a given resume hash
def get_previous_questions(resume_hash):
    conn = sqlite3.connect('data/resume_data.db')
    cursor = conn.cursor()
    
    # Get all previous questions and responses for this resume hash
    cursor.execute("SELECT question, response_generated FROM resumes WHERE resume_hash = ?", (resume_hash,))
    previous_entries = cursor.fetchall()

    conn.close()
    return previous_entries

# Function to find a similar question based on text similarity
def find_similar_question(new_question, previous_questions):
    for prev_question, prev_response in previous_questions:
        similarity_score = fuzz.ratio(new_question.lower(), prev_question.lower())
        if similarity_score > 80:  # Adjust threshold based on how strict you want the match
            return prev_question, prev_response
    return None, None

# Function to insert or append resume data as before
def insert_or_append_resume(resume_hash, skills, work_experience, industries, describe_yourself, question, response):
    conn = sqlite3.connect('data/resume_data.db')
    cursor = conn.cursor()

    # Check if the resume with the same hash already exists
    cursor.execute("SELECT id FROM resumes WHERE resume_hash = ?", (resume_hash,))
    existing_id = cursor.fetchone()

    if existing_id:
        # Resume exists, append new information as a new row but don't specify the id (let it auto-increment)
        cursor.execute(
            "INSERT INTO resumes (resume_hash, skills, work_experience, industries, describe_yourself, question, response_generated) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (resume_hash, skills, work_experience, industries, describe_yourself, question, response)
        )
        print(f"Appended new information to resume with hash {resume_hash}.")
    else:
        # Insert new record if the resume is not found
        cursor.execute(
            "INSERT INTO resumes (resume_hash, skills, work_experience, industries, describe_yourself, question, response_generated) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (resume_hash, skills, work_experience, industries, describe_yourself, question, response)
        )
        print("Inserted new resume record.")

    conn.commit()
    conn.close()
