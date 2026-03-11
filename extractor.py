import spacy
import re

nlp = spacy.load("en_core_web_sm")

skills_list = [
    "python",
    "java",
    "sql",
    "django",
    "flask",
    "machine learning",
    "data analysis",
    "html",
    "css",
    "javascript",
    "c",
    "c++",
    "git",
    "react",
    "node",
]

# ---------------------------
# EMAIL EXTRACTION
# ---------------------------

def extract_email(text):

    emails = re.findall(r'\S+@\S+', text)

    if emails:
        return emails[0]

    return "Not Found"


# ---------------------------
# PHONE EXTRACTION
# ---------------------------

def extract_phone(text):

    phones = re.findall(r'\+?\d[\d -]{8,12}\d', text)

    if phones:
        return phones[0]

    return "Not Found"


# ---------------------------
# NAME EXTRACTION
# ---------------------------

def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        if len(line.split()) <= 3 and len(line) > 2:

            return line

    return "Not Found"


# ---------------------------
# SKILL EXTRACTION
# ---------------------------

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:

            found_skills.append(skill)

    return found_skills


# ---------------------------
# EDUCATION EXTRACTION
# ---------------------------

def extract_education(text):

    education_patterns = [
        r'b\.?tech',
        r'b\.?e',
        r'bachelor',
        r'm\.?tech',
        r'master',
        r'm\.?sc',
        r'b\.?sc',
        r'ph\.?d',
        r'diploma'
    ]

    text = text.lower()

    for pattern in education_patterns:

        match = re.search(pattern, text)

        if match:

            return match.group()

    return "Not Found"


# ---------------------------
# EXPERIENCE EXTRACTION
# ---------------------------

def extract_experience(text):

    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*year',
        r'(\d+)\s*yrs'
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            return match.group()

    if "fresher" in text:

        return "Fresher"

    if "internship" in text:

        return "Internship"

    return "Not Found"