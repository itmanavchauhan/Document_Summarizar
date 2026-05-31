from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def store_in_chroma(chunks):

    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    return vector_db