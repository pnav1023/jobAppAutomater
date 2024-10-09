import os
from dotenv import load_dotenv
from pdf_parser import extract_text_from_pdf, extract_skills, extract_work_experience
from database import initialize_db, insert_or_append_resume, get_previous_questions, find_similar_question
from openai_generator import generate_response
from utils import generate_resume_hash  # Import from utils.py
from io import StringIO

# # Load environment variables from .env file

def db_connection(pdf, user_input_skills, industries_of_interest, describe_yourself, question):
    load_dotenv()
    # Step 1: Generate a hash for the uploaded resume file
    resume_hash = generate_resume_hash(pdf)

    # Step 2: Extract text from the uploaded PDF
    resume_text = extract_text_from_pdf(pdf) #StringIO(pdf).read()
    print(resume_text)
    
    # Step 3: Extract skills and work experience dynamically
    parsed_skills = extract_skills(resume_text)
    work_experience = extract_work_experience(resume_text)
    
    # Convert work_experience tuples to a string format
    formatted_work_experience = [f"{company}: {experience}" for company, experience in work_experience]
    formatted_work_experience_str = ', '.join(formatted_work_experience)

    # Step 4: Initialize the database
    initialize_db()

    # Step 5: Get additional inputs from the user
    combined_skills = parsed_skills + user_input_skills  # Combine parsed skills and user input
    
    industries_of_interest = [industry.strip() for industry in industries_of_interest]

    # Step 6: Check for similar previous questions
    previous_questions = get_previous_questions(resume_hash)
    similar_question, previous_answer = find_similar_question(question, previous_questions)

    if similar_question:
        print(f"It looks like you've asked a similar question before: '{similar_question}'")
        reuse = input("Would you like to reuse the previous answer? (yes/no): ").strip().lower()
        if reuse == 'yes':
            print("\nPrevious Answer:\n", previous_answer)
            return

    # Step 7: Generate a new response if no similar question or user wants a new one
    openai_api_key = os.getenv('OPENAI_API_KEY')  # Fetch API key from .env
    response = generate_response(openai_api_key=openai_api_key, 
                                 question=question, 
                                 skills=combined_skills, 
                                 work_experience=work_experience, 
                                 describe_yourself=describe_yourself, 
                                 industries=', '.join(industries_of_interest))

    # Step 8: Insert or append the resume record in the database
    insert_or_append_resume(resume_hash, ', '.join(combined_skills), formatted_work_experience_str, ', '.join(industries_of_interest), describe_yourself, question, response)
    
    return response
