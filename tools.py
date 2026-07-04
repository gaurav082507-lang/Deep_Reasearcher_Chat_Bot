from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from tavily import TavilyClient
import requests,os
from rich import print
from bs4 import BeautifulSoup
TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')

tavily=TavilyClient(api_key=TAVILY_API_KEY)

@tool 
def web_search(query:str)->str:
    """It searches the Query on the live web and get required
    links for the research on a given topic and some content regrading the topic
    Return the Title and URLS and a Small snippet"""
    data=tavily.search(
        query=query,
        search_depth='basic',
        max_results=5
    )
    out=[]
    for results in data['results']:
        out.append(
            f'Title :{results['title']}\nURL :{results['url']}\nSnippet :{results['content'][:300]}'
        )
    return "\n________\n.join(out)"
    
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"



    

