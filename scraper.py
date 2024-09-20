from typing import List

from llama_index.readers.web import UnstructuredURLLoader
from llama_index.core.schema import Document


def get_scraped_docs_from_urls(urls: List[str]) -> List[Document]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    loader = UnstructuredURLLoader(urls=urls, headers=headers)
    docs = loader.load_data()
    return docs
