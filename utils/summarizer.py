from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def generate_summary(text):

    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI document analyst.

        Analyze the following document and provide:

        1. A short summary
        2. Important key points
        3. Main topics discussed

        Document:
        {document}
        """
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({
        "document": text[:8000]
    })

    return response