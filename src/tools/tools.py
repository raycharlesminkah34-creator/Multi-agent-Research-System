from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
import trafilatura
import re
from readability import Document

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """Searches the web for relevant findings about a particular topic"""
    results = tavily.search(query=query, max_results=5)
    output = []
    for r in results['results']:
        output.append(
            f"Title: {r['title']}\nurl: {r['url']}\ncontent: {r['content'][: 300]}"
            )
    return "\n======\n".join(output)


def url_scrapper(url: str) -> str:
    """Downloads a webpage and extracts its main text content."""

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        html = response.text

        # Primary extraction
        content = trafilatura.extract(
            html,
            include_links=True,
            include_tables=True
        )

        # Fallback if Trafilatura fails
        if not content:
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            content = soup.get_text(separator="\n", strip=True)

        if not content:
            return "No readable content found."

        return content

    except requests.exceptions.RequestException as e:
        return f"Scraping error: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"

