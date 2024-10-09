# import os
from openai import OpenAI
import sqlite3
from database import insert_or_append_resume  # Updated to use the new function

# Function to generate the OpenAI chat response and save it in the database
def generate_response(openai_api_key, question, skills, work_experience, describe_yourself, industries):
    
    # Prepare the work experience and skills string
    work_exp_str = "\n".join([f"{company}: {experience}" for company, experience in work_experience])
    skills_str = ", ".join(skills)

    # Define the message (chat prompt) for OpenAI
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Answer the following question in 500 words: '{question}' Using my skills: {skills_str}, my work experience: {work_exp_str}, and describe myself as: {describe_yourself}"}
    ]
    client = OpenAI(
        api_key = openai_api_key
    )
    # Make the request to OpenAI's chat/completions endpoint
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
        # max_tokens=500
    )

    # Extract the response text
    response_text = response.choices[0].message.content.strip()

    # Return the response text to be inserted into the database
    return response_text
