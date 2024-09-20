import os
from typing import List
import requests
from dotenv import load_dotenv


async def get_urls_from_tavily_search(sub_query: str) -> List[str]:
    load_dotenv()
    api_key = os.getenv("TAVILY_API_KEY")
    base_url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "query": sub_query,
        "api_key": api_key,
    }

    response = requests.post(base_url, headers=headers, json=data)
    if response.status_code == 200:
        search_results = response.json().get("results", [])
        search_urls = [result.get("url") for result in search_results]
        return search_urls
    else:
        response.raise_for_status()
