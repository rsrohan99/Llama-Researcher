import os
from typing import List
import requests
from dotenv import load_dotenv


async def get_urls_from_tavily_search(sub_query: str) -> List[str]:
    return [
        "https://dl.acm.org/doi/fullHtml/10.1145/3530775",
        "https://www.researchgate.net/publication/360109644_FPGA_HLS_Today_Successes_Challenges_and_Opportunities",
        "https://semiengineering.com/challenges-in-using-hls-for-fpga-design/",
        "https://www.academia.edu/98536271/FPGA_HLS_Today_Successes_Challenges_and_Opportunities",
        "https://www.fccm.org/past/2020/proceedings/2020/pdfs/FCCM2020-65FOvhMqzyMYm99lfeVKyl/580300a195/580300a195.pdf",
    ]
    # load_dotenv()
    # api_key = os.getenv("TAVILY_API_KEY")
    # base_url = "https://api.tavily.com/search"
    # headers = {
    #     "Content-Type": "application/json",
    # }
    # data = {
    #     "query": sub_query,
    #     "api_key": api_key,
    # }

    # response = requests.post(base_url, headers=headers, json=data)
    # if response.status_code == 200:
    #     search_results = response.json().get("results", [])
    #     search_urls = [result.get("url") for result in search_results]
    #     return search_urls
    # else:
    #     response.raise_for_status()
