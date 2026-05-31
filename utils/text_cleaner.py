import re


def clean_extracted_text(text):

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Add line breaks after periods
    text = re.sub(r'\.\s', '.\n\n', text)

    # Add line breaks before bullets
    text = re.sub(r'•', '\n• ', text)

    # Fix multiple newlines
    text = re.sub(r'\n+', '\n\n', text)

    return text.strip()