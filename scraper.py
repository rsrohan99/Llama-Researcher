from typing import List
import requests
from io import BytesIO
import os

from llama_index.readers.web import FireCrawlWebReader
from llama_index.core.schema import Document
from llama_parse import LlamaParse
from dotenv import load_dotenv


def get_scraped_docs_from_urls(urls: List[str]) -> List[Document]:
    load_dotenv()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    docs = []
    idx = 0
    for url in urls:
        initial_resp = requests.get(url, headers=headers)
        if (
            initial_resp.status_code == 200
            and initial_resp.headers["Content-Type"] == "application/pdf"
        ):
            parser = LlamaParse()
            file_input = BytesIO(initial_resp.content)
            print(f"\n> Found PDF from {url}, parsing using LlamaParse...\n")
            docs.extend(
                parser.load_data(file_input, extra_info={"file_name": f"url_{idx}.pdf"})
            )
            idx += 1
        else:
            reader = FireCrawlWebReader(api_key=os.environ.get("FIRECRAWL_API_KEY"))
            print(f"\n> Scraping ${url} using FireCrawl...\n")
            docs.extend(reader.load_data(url=url))

    return docs
