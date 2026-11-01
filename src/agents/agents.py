from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, url_scrapper
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

def build_search_agent(): 
    search_agent = create_agent(
        model=llm,
        tools=[web_search],
    )

    return search_agent



def build_reader_agent():
    reader_agent = create_agent(
        model=llm,
        tools=[url_scrapper]
    )

    return reader_agent
