import re

def clean_resume(text):
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'RT|cc', ' ', text)
    text = re.sub(r'#\S+', ' ', text)
    text = re.sub(r'@\S+', ' ', text)
    text = re.sub(r'[^A-Za-z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.lower().strip()