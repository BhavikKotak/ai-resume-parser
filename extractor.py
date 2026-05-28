import re

SKILLS_LIST = [
    "python",
    "java",
    "sql",
    "mysql",
    "sqlite",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "bootstrap",
    "react",
    "node",
    "git",
    "github",
    "c",
    "c++",
    "php",
    "pandas",
    "numpy",
    "excel",
    "power bi"
]


def extract_email(text):
    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )
    return emails[0] if emails else "Not Found"


def extract_phone(text):
    phones = re.findall(
        r'(\+?\d[\d\s\-]{8,15})',
        text
    )
    return phones[0] if phones else "Not Found"


def extract_name(text):
    lines = text.split("\n")

    for line in lines[:8]:
        line = line.strip()

        if (
            len(line.split()) <= 4
            and len(line) > 3
            and "resume" not in line.lower()
        ):
            return line

    return "Not Found"


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS_LIST:
        if skill in text:
            found.append(skill)

    return list(set(found))


def extract_education(text):
    patterns = [
        r'b\.?tech',
        r'b\.?e',
        r'bachelor',
        r'm\.?tech',
        r'master',
        r'diploma',
        r'engineering'
    ]

    text = text.lower()

    found = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        found.extend(matches)

    return ", ".join(list(set(found))) if found else "Not Found"


def extract_experience(text):
    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*year',
        r'(\d+)\s*months'
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


def extract_linkedin(text):
    match = re.search(
        r'https?://(www\.)?linkedin\.com/in/[^\s]+',
        text
    )
    return match.group() if match else "Not Found"


def extract_github(text):
    match = re.search(
        r'https?://(www\.)?github\.com/[^\s]+',
        text
    )
    return match.group() if match else "Not Found"


def extract_certifications(text):
    keywords = [
        "certificate",
        "certification",
        "aws",
        "coursera",
        "udemy"
    ]

    found = []

    lower = text.lower()

    for keyword in keywords:
        if keyword in lower:
            found.append(keyword)

    return ", ".join(found) if found else "Not Found"


def extract_projects(text):
    if "project" in text.lower():
        return "Project Section Found"

    return "Not Found"


def extract_address(text):
    lines = text.split("\n")

    keywords = ["road", "street", "india", "gujarat"]

    for line in lines[:20]:
        for keyword in keywords:
            if keyword in line.lower():
                return line.strip()

    return "Not Found"