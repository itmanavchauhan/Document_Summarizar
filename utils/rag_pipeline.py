from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def ask_question(question, vector_db):

    # Retrieve relevant chunks
    docs = vector_db.similarity_search(
        question,
        k=5
    )

    print("\nRetrieved Chunks:\n")

    for doc in docs:
        print(doc.page_content)
        print("\n-----------------\n")

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI assistant answering questions from uploaded documents.

        Use ONLY the provided context to answer.

        If the answer is not found in the context,
        say:
        "Answer not available in uploaded documents."

        Context:
        {context}

        Question:
        {question}
        """
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response