import re

def extract_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    emails = re.findall(email_pattern, text)

    return emails[0] if emails else "Not Found"


def extract_phone(text):
    phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'

    phones = re.findall(phone_pattern, text)

    return phones[0] if phones else "Not Found"


def extract_name(text):
    lines = text.split('\n')

    for line in lines:
        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return "Not Found"