import re
import nltk

from nltk.tokenize import sent_tokenize

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Download punkt tokenizer
nltk.download('punkt')


# =========================
# SMART TEXT PROCESSING
# =========================

def process_text(text):

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove strange unicode characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Fix bullet points
    text = text.replace("•", "\n• ")

    # Sentence segmentation
    sentences = sent_tokenize(text)

    cleaned_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 2:
            cleaned_sentences.append(sentence)

    # Rebuild text properly
    final_text = "\n\n".join(cleaned_sentences)

    return final_text


# =========================
# RAG CHUNKING
# =========================

def create_chunks(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_text(text)

    return chunks