import re

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def find_keywords(text):
    keywords = set()
    for word in text.split():
        keywords.update(camel_case_split(word))
    return keywords
