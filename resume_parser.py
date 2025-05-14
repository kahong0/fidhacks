import PyPDF2
import re

# formats skills txt into a set
def get_skills(file_path="skills.txt"):
    skills = []

    with open(file_path, "r") as file:
        for line in file:
            if line.strip() != '':
                skills.append(line.strip().lower())
    
    return set(skills) # set to avoid duplicates


# extracts text from pdf
def text_extraction(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


# parses key skills from text using regex
def parse_skills(text, skills):
    matched_skills = set()
    text = text.lower()
    for skill in skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            matched_skills.add(skill)
    return matched_skills


if __name__ == "__main__":
    file_path = "Sample_Resume.pdf"
    all_skills = get_skills("skills.txt")
    pdf_text = text_extraction(file_path)
    matched_skills = parse_skills(pdf_text, all_skills)

    print("\nMatched Skills:")
    for skill in sorted(matched_skills):
        print("-", skill)
        