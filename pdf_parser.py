import PyPDF2

def extract_text_from_pdf(pdf_path):
    #with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(pdf_path)
    text = ''
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def extract_skills(text):
    # Example: Locate the 'Top Skills' section dynamically
    skills_start = text.find('Top Skills') + len('Top Skills')
    skills_end = text.find('Experience')
    skills_text = text[skills_start:skills_end].strip()

    # Split the skills by newline or comma and clean them
    skills = skills_text.split("\n")
    return [skill.strip() for skill in skills if skill.strip()]

def extract_work_experience(text):
    # Locate 'Experience' and 'Education' sections dynamically
    work_exp_start = text.find('Experience') + len('Experience')
    work_exp_end = text.find('Education')
    work_exp_text = text[work_exp_start:work_exp_end].strip()

    companies = []
    experience_details = []
    lines = work_exp_text.split('\n')

    # Flags to track when we are in the company and experience sections
    current_company = None
    current_experience = []

    # Extract companies and their experience descriptions
    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line and "•" not in stripped_line:  # This is likely a company or job title line
            if current_company:
                # Append the previous company with its experience details
                companies.append((current_company, " ".join(current_experience)))
            # Start a new company entry
            current_company = stripped_line
            current_experience = []
        elif "•" in stripped_line:  # This is likely an experience detail line
            current_experience.append(stripped_line)
    
    # Append the last company and experience
    if current_company:
        companies.append((current_company, " ".join(current_experience)))

    return companies
