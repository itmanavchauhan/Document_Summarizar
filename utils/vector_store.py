import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def store_in_chroma(chunks):
    
    # Delete old vector DB
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")

    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    vector_db.persist()

    return vector_db


def load_chroma():

    vector_db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    return vector_db