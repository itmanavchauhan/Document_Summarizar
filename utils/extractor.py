from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def extract_information(text):

    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI information extraction system.

        Extract the following information from the document.

        Return properly formatted sections.

        Extract:
        - Important Names
        - Dates
        - Organizations
        - Emails
        - Technologies
        - Key Topics
        - Action Items
        - Important Keywords

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